use std::sync::mpsc::RecvError;

#[derive(Debug)]
pub enum Error {
    ChannelError(RecvError),
}

impl From<RecvError> for Error {
    fn from(error: RecvError) -> Self {
        Self::ChannelError(error)
    }
}
