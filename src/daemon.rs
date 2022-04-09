use std::{
    collections::HashMap,
    process::{Child, Command, Stdio},
    sync::mpsc::Receiver,
};

use crate::{config::Config, error::Error, message::DaemonMessage, types::*};

pub struct Daemon {
    config: Config,
    processes: HashMap<TrsyncUid, Child>,
}

impl Daemon {
    pub fn new(config: Config) -> Self {
        Self {
            config,
            processes: HashMap::new(),
        }
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
        // WIP
        for (process_uid, child) in &mut self.processes {
            log::info!("kill {}", child.id());
            match child.kill() {
                Err(_) => {
                    log::info!("Process of {:?} was not running", process_uid)
                }
                _ => {
                    log::info!("ok kill");
                }
            }
            child.wait().expect("foo");
        }

        let child = Command::new("sleep")
            .arg("100")
            .stdout(Stdio::null())
            .spawn()
            .expect("failed to execute process");
        self.processes
            .insert(TrsyncUid::new("foo".to_string(), 42), child);

        Ok(())
    }
}
