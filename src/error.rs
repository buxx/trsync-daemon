use std::sync::mpsc::RecvError;

#[derive(Debug)]
pub enum Error {
    ChannelError(RecvError),
    UnableToFindHomeUser,
    ReadConfigError(String),
    FailToSpawnTrsyncProcess,
}

impl From<RecvError> for Error {
    fn from(error: RecvError) -> Self {
        Self::ChannelError(error)
    }
}

#[derive(Debug)]
pub enum ClientError {
    RequestError(String),
    Unauthorized,
    UnexpectedResponse(String),
    NotFoundResponse(String),
}

impl From<reqwest::Error> for ClientError {
    fn from(error: reqwest::Error) -> Self {
        Self::RequestError(format!("Error happen when make request : {:?}", error))
    }
}
