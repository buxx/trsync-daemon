use std::sync::mpsc::Receiver;

use crate::{config::Config, error::Error, message::DaemonMessage};

pub struct Daemon {
    config: Config,
}

impl Daemon {
    pub fn new(config: Config) -> Self {
        Self { config }
    }

    pub fn run(&mut self, reload_channel: Receiver<DaemonMessage>) -> Result<(), Error> {
        self.ensure_processes()?;

        loop {
            // Blocking until new message received
            match reload_channel.recv() {
                Ok(DaemonMessage::ReloadFromConfig(new_config)) => {
                    self.config = new_config;
                    self.ensure_processes()?
                }
                Ok(DaemonMessage::Stop) => break,
                Err(error) => return Err(Error::from(error)),
            }
        }

        Ok(())
    }

    pub fn ensure_processes(&mut self) -> Result<(), Error> {
        log::info!("coucou");
        Ok(())
    }
}
