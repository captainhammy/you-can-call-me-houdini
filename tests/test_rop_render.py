"""Tests for the you_can_call_me_houdini.rop_render module."""

# Third Party
import humanfriendly
import pytest

# You Can Call Me Houdini
import you_can_call_me_houdini.rop_render

# Houdini
import hou

pytestmark = pytest.mark.usefixtures("load_module_test_hip_file")


# Tests


class TestRopRenderProcess:
    """Test the you_can_call_me_houdini.rop_render.RopRenderProcess object."""

    @pytest.mark.parametrize(
        "node_path,has_output_parm",
        (
            ("/out/geometry", True),
            ("/out/comp", False),
            ("/out/alembic", False),
        ),
    )
    def test_init(self, monkeypatch, node_path, has_output_parm):
        """Test object initialization/post initialization."""
        # Remove/alter items in the output parameter mapping to test expected behaviors.
        monkeypatch.delitem(
            you_can_call_me_houdini.rop_render._FILE_PARM_MAP, "Driver/comp"
        )
        monkeypatch.setitem(
            you_can_call_me_houdini.rop_render._FILE_PARM_MAP, "Driver/alembic", "foo"
        )

        test_node = hou.node(node_path)

        process = you_can_call_me_houdini.rop_render.RopRenderProcess(test_node)

        assert process.node == test_node

        if has_output_parm:
            assert isinstance(process.output_parameter, hou.Parm)

        else:
            assert process.output_parameter is None

        assert process.has_post_write == bool(test_node.parm("postwrite") is not None)

    @pytest.mark.parametrize("has_output_parm", (False, True))
    def test_pre_render(self, mocker, has_output_parm):
        """Test RopRenderProcess.pre_render()."""
        mock_emit = mocker.patch.object(
            you_can_call_me_houdini.rop_render.CallbackManager, "emit"
        )

        mock_get_padding = mocker.patch(
            "you_can_call_me_houdini.rop_render._get_frame_padding"
        )

        mock_node = mocker.MagicMock(spec=hou.RopNode)

        event_args = {"scene_time": 123}

        inst = you_can_call_me_houdini.rop_render.RopRenderProcess(mock_node)

        mock_output_parm = mocker.MagicMock(spec=hou.Parm)

        if has_output_parm:
            inst.output_parameter = mock_output_parm

        inst.pre_render(event_args)

        mock_emit.assert_called_with(
            you_can_call_me_houdini.rop_render.RopRenderEvent.PreRender,
            {
                "process": inst,
                "node": mock_node,
                "scene_time": event_args["scene_time"],
                "render_count": inst.render_count,
                "render_start_time": inst.render_start_time,
            },
        )

        if has_output_parm:
            assert inst.frame_padding == mock_get_padding.return_value

    @pytest.mark.parametrize("has_output_parm", (False, True))
    def test_pre_frame(self, mocker, has_output_parm):
        """Test RopRenderProcess.pre_frame()."""
        mock_emit = mocker.patch.object(
            you_can_call_me_houdini.rop_render.CallbackManager, "emit"
        )

        mock_node = mocker.MagicMock(spec=hou.RopNode)

        event_args = {"scene_time": 123}

        inst = you_can_call_me_houdini.rop_render.RopRenderProcess(mock_node)

        mock_output_parm = mocker.MagicMock(spec=hou.Parm)

        if has_output_parm:
            inst.output_parameter = mock_output_parm

        inst.pre_frame(event_args)

        assert inst.frame_start_time > 0

        expected_args = {
            "process": inst,
            "node": mock_node,
            "scene_time": event_args["scene_time"],
            "render_count": inst.render_count,
            "render_start_time": inst.render_start_time,
            "frame_start_time": inst.frame_start_time,
            "frame_padding": inst.frame_padding,
        }

        if has_output_parm:
            expected_args["output_path"] = mock_output_parm.evalAtTime.return_value

        mock_emit.assert_called_with(
            you_can_call_me_houdini.rop_render.RopRenderEvent.PreFrame,
            expected_args,
        )

    @pytest.mark.parametrize("has_output_parm", (False, True))
    def test_post_frame(self, mocker, has_output_parm):
        """Test RopRenderProcess.post_frame()."""
        mock_emit = mocker.patch.object(
            you_can_call_me_houdini.rop_render.CallbackManager, "emit"
        )

        mock_node = mocker.MagicMock(spec=hou.RopNode)

        mocker.patch("time.time", return_value=789)

        event_args = {"scene_time": 123}

        inst = you_can_call_me_houdini.rop_render.RopRenderProcess(mock_node)
        inst.frame_start_time = 456

        mock_output_parm = mocker.MagicMock(spec=hou.Parm)

        if has_output_parm:
            inst.output_parameter = mock_output_parm

        inst.post_frame(event_args)

        expected_args = {
            "process": inst,
            "node": mock_node,
            "scene_time": event_args["scene_time"],
            "render_count": inst.render_count,
            "render_start_time": inst.render_start_time,
            "frame_start_time": inst.frame_start_time,
            "frame_padding": inst.frame_padding,
            "frame_end_time": 789,
            "frame_time": 789 - 456,
        }

        if has_output_parm:
            expected_args["output_path"] = mock_output_parm.evalAtTime.return_value

        mock_emit.assert_called_with(
            you_can_call_me_houdini.rop_render.RopRenderEvent.PostFrame,
            expected_args,
        )

    def test_post_render(self, mocker):
        """Test RopRenderProcess.post_render()."""
        mock_emit = mocker.patch.object(
            you_can_call_me_houdini.rop_render.CallbackManager, "emit"
        )

        mock_node = mocker.MagicMock(spec=hou.RopNode)

        mocker.patch("time.time", return_value=789)

        event_args = {"scene_time": 123}

        inst = you_can_call_me_houdini.rop_render.RopRenderProcess(mock_node)

        inst.render_start_time = 456

        inst.post_render(event_args)

        mock_emit.assert_called_with(
            you_can_call_me_houdini.rop_render.RopRenderEvent.PostRender,
            {
                "process": inst,
                "node": mock_node,
                "scene_time": event_args["scene_time"],
                "render_count": inst.render_count,
                "render_start_time": 456,
                "render_end_time": 789,
                "render_time": 789 - 456,
            },
        )

    @pytest.mark.parametrize("has_output_parm", (False, True))
    def test_post_write(self, mocker, has_output_parm):
        """Test RopRenderProcess.post_write()."""
        mock_emit = mocker.patch.object(
            you_can_call_me_houdini.rop_render.CallbackManager, "emit"
        )

        mock_node = mocker.MagicMock(spec=hou.RopNode)

        event_args = {"scene_time": 123}

        inst = you_can_call_me_houdini.rop_render.RopRenderProcess(mock_node)

        mock_output_parm = mocker.MagicMock(spec=hou.Parm)

        if has_output_parm:
            inst.output_parameter = mock_output_parm

        inst.post_write(event_args)

        expected_args = {
            "process": inst,
            "node": mock_node,
            "scene_time": event_args["scene_time"],
        }

        if has_output_parm:
            expected_args["output_path"] = mock_output_parm.evalAtTime.return_value

        mock_emit.assert_called_with(
            you_can_call_me_houdini.rop_render.RopRenderEvent.PostWrite,
            expected_args,
        )


class TestRopRenderFactory:
    """Test the you_can_call_me_houdini.rop_render.RopRenderFactory object."""

    @pytest.mark.parametrize("exists", (False, True))
    def test_get_process_for_node(self, monkeypatch, mocker, exists):
        """Test RopRenderFactory.get_process_for_node()"""
        mock_node = mocker.MagicMock(spec=hou.RopNode)

        inst = you_can_call_me_houdini.rop_render.RopRenderFactory()
        inst._node_processes.clear()

        existing = you_can_call_me_houdini.rop_render.RopRenderProcess(mock_node)

        if exists:
            inst._node_processes[mock_node] = existing
        assert len(inst._node_processes) == (1 if exists else 0)

        result = inst.get_process_for_node(mock_node)

        if exists:
            assert result is existing

        else:
            assert result is not existing

        assert len(inst._node_processes) == 1


def test__find_all_rop_instances():
    """Test you_can_call_me_houdini.rop_render._find_all_rop_instances()."""
    result = you_can_call_me_houdini.rop_render._find_all_rop_instances()

    # Note: If the test scene is updated, ensure this number is adjusted to match
    # new/removed ROP nodes.
    assert len(result) == 12


@pytest.mark.parametrize(
    "parameter_path, expected",
    (
        ("/out/test__get_frame_padding/test_reference_f4/sopoutput", 4),
        ("/out/test__get_frame_padding/test_f3/sopoutput", 3),
        ("/out/test__get_frame_padding/test_f/sopoutput", 1),
        ("/out/test__get_frame_padding/test_expression/sopoutput", 1),
        ("/out/test__get_frame_padding/test_no_frame/sopoutput", 1),
    ),
)
def test__get_frame_padding(parameter_path, expected):
    """Test you_can_call_me_houdini.rop_render._get_frame_padding()."""
    parameter = hou.parm(parameter_path)

    result = you_can_call_me_houdini.rop_render._get_frame_padding(parameter)

    assert result == expected


def test_attach_rop_render_event(mocker):
    """Test you_can_call_me_houdini.rop_render.attach_rop_render_event()."""
    # Test a proper ROP node.
    mock_rop_node = mocker.MagicMock(spec=hou.RopNode)
    you_can_call_me_houdini.rop_render.attach_rop_render_event({"node": mock_rop_node})
    mock_rop_node.addRenderEventCallback.assert_called_with(
        you_can_call_me_houdini.rop_render.handle_rop_render_event
    )

    # Test something not a ROP node, ensuring we don't try and call a non-existent method on it.
    mock_non_rop_node = mocker.MagicMock()
    you_can_call_me_houdini.rop_render.attach_rop_render_event(
        {"node": mock_non_rop_node}
    )
    mock_non_rop_node.addRenderEventCallback.assert_not_called()


def test_attach_rop_render_to_all_nodes(mocker):
    """Test you_can_call_me_houdini.rop_render.attach_rop_render_to_all_nodes()."""
    mock_rop1 = mocker.MagicMock(spec=hou.RopNode)
    mock_rop2 = mocker.MagicMock(spec=hou.RopNode)

    mocker.patch(
        "you_can_call_me_houdini.rop_render._find_all_rop_instances",
        return_value=[mock_rop1, mock_rop2],
    )

    you_can_call_me_houdini.rop_render.attach_rop_render_to_all_nodes({})

    mock_rop1.addRenderEventCallback.assert_called_with(
        you_can_call_me_houdini.rop_render.handle_rop_render_event
    )
    mock_rop2.addRenderEventCallback.assert_called_with(
        you_can_call_me_houdini.rop_render.handle_rop_render_event
    )


@pytest.mark.parametrize(
    "render_type,has_post_write",
    (
        (hou.ropRenderEventType.PreRender, False),
        (hou.ropRenderEventType.PreFrame, False),
        (hou.ropRenderEventType.PostFrame, False),
        (hou.ropRenderEventType.PostFrame, True),
        (hou.ropRenderEventType.PostWrite, False),
        (hou.ropRenderEventType.PostRender, False),
        (None, False),
    ),
)
def test_handle_rop_render_event(mocker, out_test_node, render_type, has_post_write):
    """Test you_can_call_me_houdini.rop_render.handle_rop_render_event()."""
    mock_process = mocker.MagicMock(
        spec=you_can_call_me_houdini.rop_render.RopRenderProcess
    )
    mock_process.has_post_write = has_post_write

    mocker.patch.object(
        you_can_call_me_houdini.rop_render.RopRenderFactory,
        "get_process_for_node",
        return_value=mock_process,
    )

    you_can_call_me_houdini.rop_render.handle_rop_render_event(
        out_test_node, render_type, 1.0
    )

    if render_type == hou.ropRenderEventType.PostFrame and not has_post_write:
        mock_process.post_write.assert_called()


def test_print_pre_render(mocker):
    """Test you_can_call_me_houdini.rop_render.print_pre_render()."""
    mock_print = mocker.patch("builtins.print")

    mock_node = mocker.MagicMock(spec=hou.RopNode)
    mock_node.path.return_value = "/out/test_node"

    test_args = {"node": mock_node}

    you_can_call_me_houdini.rop_render.print_pre_render(test_args)

    mock_print.assert_called_with("Starting Render /out/test_node")


@pytest.mark.parametrize(
    "scene_time, expected_frame",
    (
        (0.375, "0010"),
        (1.1234, "27.962"),
    ),
)
def test_print_post_frame(mocker, scene_time, expected_frame):
    """Test you_can_call_me_houdini.rop_render.print_post_frame()."""
    mock_print = mocker.patch("builtins.print")

    mock_node = mocker.MagicMock(spec=hou.RopNode)
    mock_node.path.return_value = "/out/test_node"

    test_args = {
        "node": mock_node,
        "scene_time": scene_time,
        "frame_padding": 4,
        "frame_time": 1.23456,
    }

    you_can_call_me_houdini.rop_render.print_post_frame(test_args)

    mock_print.assert_called_with(f"Frame {expected_frame} complete 1.235s")


@pytest.mark.parametrize(
    "output_path",
    (
        "/output/path/test.bgeo",
        "temp:test.bgeo",
        None,
    ),
)
def test_print_post_write(mocker, output_path):
    """Test you_can_call_me_houdini.rop_render.print_post_write()."""
    mock_stat = mocker.MagicMock()
    mock_stat.st_size = 123456

    mocker.patch("pathlib.Path.stat", return_value=mock_stat)
    mock_print = mocker.patch("builtins.print")

    mock_node = mocker.MagicMock(spec=hou.RopNode)
    mock_node.path.return_value = "/out/test_node"

    test_args = {
        "node": mock_node,
    }

    if output_path is not None:
        test_args["output_path"] = output_path

    you_can_call_me_houdini.rop_render.print_post_write(test_args)

    if output_path and not output_path.startswith("temp:"):
        mock_print.assert_called_with(
            f"Wrote {output_path} ({humanfriendly.format_size(mock_stat.st_size)})"
        )
    else:
        mock_print.assert_not_called()


def test_print_post_render(mocker):
    """Test you_can_call_me_houdini.rop_render.print_post_render()."""
    mock_print = mocker.patch("builtins.print")

    mock_node = mocker.MagicMock(spec=hou.RopNode)
    mock_node.path.return_value = "/out/test_node"

    test_args = {"node": mock_node, "render_count": 2, "render_time": 1.23456}

    you_can_call_me_houdini.rop_render.print_post_render(test_args)

    mock_print.assert_called_with("Finished Rendering /out/test_node: 2 total 1.235s")
