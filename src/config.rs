use ini::Ini;

use crate::error::Error;

#[derive(Debug, Clone)]
pub struct Config {}
impl Config {
    pub fn from_env() -> Result<Self, Error> {
        let user_home_folder_path = match dirs::home_dir() {
            Some(folder) => folder,
            None => return Err(Error::UnableToFindHomeUser),
        };
        let config_file_path = if cfg!(target_os = "windows") {
            user_home_folder_path
                .join("AppData")
                .join("trsync")
                .join("trsync.conf")
        } else {
            user_home_folder_path.join(".trsync.conf")
        };

        let config_ini = match Ini::load_from_file(config_file_path) {
            Ok(content) => content,
            Err(error) => {
                return Err(Error::ReadConfigError(format!(
                    "Unable to read or load '{:?}' config file : {}",
                    config_file_path, error,
                )))
            }
        };
        Self::from_ini(config_ini)
    }

    pub fn from_ini(config_ini: Ini) -> Result<Self, Error> {
        Ok(Self {})
    }
}
