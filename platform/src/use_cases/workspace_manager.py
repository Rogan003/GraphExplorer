def get_workspaces(session):
    return session.get("workspaces", [])

def add_workspace(session, workspace):
    workspaces = get_workspaces(session)
    workspaces.append({
        "id": workspace.id,
        "file_path": workspace.file_path,
        "data_source_identifier": workspace.data_source_identifier,
        "visualizer_identifier": workspace.visualizer_identifier,
    })
    session["workspaces"] = workspaces
    session.modified = True

def update_workspace(session, index, workspace):
    workspaces = get_workspaces(session)
    workspaces[index] = workspace.__dict__
    session.modified = True