from django.core.files.storage import FileSystemStorage
from use_cases.workspace.workspace import Workspace

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
    If there are no workspaces in the session, create an empty workspace.
    Returns the list of workspaces.
    """
    workspaces = _get_workspaces(session)
    if not workspaces:
        ws = Workspace(id=0)
        ws.load_graph(plugin_service, tree_view_service)
        _add_workspace(session, ws)
        workspaces = _get_workspaces(session)
    return workspaces

def upload_file(request):
    """
    Uploads a file from a POST request. Returns the file path or None.
    """
    if request.method == "POST" and request.FILES.get("file"):
        fs = FileSystemStorage()
        filename = fs.save(request.FILES["file"].name, request.FILES["file"])
        return fs.path(filename)
    return None

def get_active_workspace(session, ws_id, path=None, datasource=None, visualizer=None, plugin_service=None, tree_view_service=None,
                         data_source_config=None):
    """
    Loads the workspace with the given ID and updates its parameters.
    Returns the Workspace object and the list of workspaces.
    """
    workspaces = _get_workspaces(session)
    if not workspaces or not (0 <= ws_id < len(workspaces)):
        return None, workspaces

    ws_dict = workspaces[ws_id]
    ws = Workspace(**ws_dict)
    ws.tree_view = tree_view_service.empty_tree()
    if path:
        ws.path = path
    if datasource:
        ws.data_source_identifier = datasource
    if visualizer:
        ws.visualizer_identifier = visualizer
    if plugin_service and tree_view_service:
        ws.load_graph(plugin_service, tree_view_service)
    if data_source_config:
        ws.configuration.update(**data_source_config)

    _update_workspace_in_session(session, ws)
    workspaces = _get_workspaces(session)
    return ws, workspaces

def create_workspace(session, path=None, datasource=None, visualizer=None, plugin_service=None, tree_view_service=None,
                     data_source_config=None):
    """
    Creates a new workspace, loads the graph if plugins are provided, adds it to the session.
    Returns the Workspace object and the list of workspaces.
    """
    workspaces = _get_workspaces(session)
    ws = Workspace(
        id=len(workspaces),
        path=path,
        data_source_identifier=datasource,
        visualizer_identifier=visualizer,
        data_source_configuration=data_source_config
    )
    ws.tree_view = tree_view_service.empty_tree()
    if plugin_service and tree_view_service:
        ws.load_graph(plugin_service, tree_view_service)
    _add_workspace(session, ws)
    workspaces = _get_workspaces(session)
    return ws, workspaces
