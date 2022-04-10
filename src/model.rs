#[derive(Debug, Clone)]
pub struct Instance {
    pub name: String,
    pub address: String,
    pub unsecure: bool,
    pub username: String,
    pub password: String,
    pub workspaces_ids: Vec<u32>,
}

#[derive(Debug, Clone)]
pub struct Workspace {
    pub name: String,
    pub id: u32,
}
