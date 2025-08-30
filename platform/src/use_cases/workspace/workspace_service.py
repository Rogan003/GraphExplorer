from django.core.files.storage import FileSystemStorage
from use_cases.workspace.workspace import Workspace
from graph_explorer_api.model.graph import Graph
# import pdb

def _get_workspaces(session):
    return session.get("workspaces", [])

def _add_workspace(session, workspace):
    workspaces = _get_workspaces(session)
    workspaces.append(workspace.to_dict())
    session["workspaces"] = workspaces
    session.modified = True

def _update_workspace_in_session(session, ws):
    workspaces = _get_workspaces(session)
    if 0 <= ws.id < len(workspaces):
        workspaces[ws.id] = ws.to_dict()
        session["workspaces"] = workspaces
        session.modified = True


def handle_initial_workspace(session, plugin_service, tree_view_service):
    """
    Initialize the session with a default workspace if none exist.

    Args:
        session (Session): Django session object where workspaces are stored.
        plugin_service: Service used for loading and rendering the graph.
        tree_view_service: Service used for generating the tree view.

    Returns:
        list[dict]: List of serialized workspaces stored in the session.
    """
    workspaces = _get_workspaces(session)
    if not workspaces:
        ws = Workspace(id=0)
        ws.load_graph(plugin_service, tree_view_service)
        ws.show_graph(plugin_service, tree_view_service)
        _add_workspace(session, ws)
        workspaces = _get_workspaces(session)
    return workspaces

def upload_file(request):
    """
    Handle file upload from a POST request.

    Args:
        request (HttpRequest): Django request object containing uploaded file.

    Returns:
        str | None: Absolute file path of the saved file if upload succeeds,
        otherwise None.
    """
    if request.method == "POST" and request.FILES.get("file"):
        fs = FileSystemStorage()
        filename = fs.save(request.FILES["file"].name, request.FILES["file"])
        return fs.path(filename)
    return None

def get_active_workspace(session, ws_id, visualizer=None, datasource=None, plugin_service=None, tree_view_service=None, file_path=None):
    """
    Load and update a workspace by ID, optionally updating its parameters.

    Args:
        session (Session): Django session object where workspaces are stored.
        ws_id (int): ID of the workspace to load.
        visualizer (str, optional): Visualizer identifier to set.
        datasource (str, optional): Data source identifier to set.
        plugin_service (optional): Service used for loading and rendering the graph.
        tree_view_service (optional): Service used for generating the tree view.
        file_path (str, optional): Path to the graph data file.

    Returns:
        tuple[Workspace | None, list[dict]]:
            - Workspace instance if found, otherwise None.
            - List of serialized workspaces currently in the session.
    """
    workspaces = _get_workspaces(session)
    if not workspaces or not (0 <= ws_id < len(workspaces)):
        return None, workspaces

    ws_dict = workspaces[ws_id].copy()
    ws_dict.pop("graph", None)
    
    ws = Workspace(**ws_dict)

    if "graph_data" in ws_dict and ws_dict["graph_data"] is not None:
        ws.graph = Graph.from_dict(ws_dict["graph_data"])

    if visualizer:
        ws.visualizer_identifier = visualizer
    if datasource:
        ws.data_source_identifier = datasource
    if file_path:
        ws.file_path = file_path

    if plugin_service and tree_view_service:
        if ws.graph is None or not ws.graph.nodes:
            ws.load_graph(plugin_service, tree_view_service)
        ws.graph_html = ws.show_graph(plugin_service, tree_view_service)

    _update_workspace_in_session(session, ws)
    workspaces = _get_workspaces(session)
    return ws, workspaces

def create_workspace(session, file_path=None, datasource=None, visualizer=None, plugin_service=None, tree_view_service=None):
    """
    Create a new workspace and add it to the session.

    Args:
        session (Session): Django session object where workspaces are stored.
        file_path (str, optional): Path to the graph data file.
        datasource (str, optional): Data source identifier.
        visualizer (str, optional): Visualizer identifier.
        plugin_service (optional): Service used for loading and rendering the graph.
        tree_view_service (optional): Service used for generating the tree view.

    Returns:
        tuple[Workspace, list[dict]]:
            - Newly created Workspace instance.
            - List of serialized workspaces currently in the session.
    """
    workspaces = _get_workspaces(session)
    ws = Workspace(
        id=len(workspaces),
        file_path=file_path,
        data_source_identifier=datasource,
        visualizer_identifier=visualizer,
    )

    if plugin_service and tree_view_service:
        if ws.graph is None:
            ws.load_graph(plugin_service, tree_view_service)
        ws.graph_html = ws.show_graph(plugin_service, tree_view_service)

    _add_workspace(session, ws)
    workspaces = _get_workspaces(session)
    return ws, workspaces

def save_workspace(session, ws):
    """
    Persist the given workspace into the session.

    Ensures that the graph data is serialized before saving.

    Args:
        session (Session): Django session object where workspaces are stored.
        ws (Workspace): Workspace instance to save.

    Returns:
        None
    """
    ws.graph_data = ws.graph.to_dict()
    _update_workspace_in_session(session, ws)

