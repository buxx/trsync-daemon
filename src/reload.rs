use std::{
    sync::mpsc::{channel, Receiver},
    thread,
    time::Duration,
};

use crate::{config::Config, error::Error, message::DaemonMessage};

pub struct ReloadWatcher {
    config: Config,
}

impl ReloadWatcher {
    pub fn new(config: Config) -> Self {
        Self { config }
    }

    pub fn watch(&mut self) -> Result<Receiver<DaemonMessage>, Error> {
        let (sender, receiver) = channel();

        thread::spawn(move || {
            // For now, simulate reload each 10s
            loop {
                thread::sleep(Duration::from_secs(10));
                match sender.send(DaemonMessage::ReloadFromConfig(Config::new())) {
                    Err(error) => {
                        log::error!("Channel was closed when try to send message, close thread");
                        break;
                    }
                    _ => {}
                }
            }
        });

        Ok(receiver)
    }
}
