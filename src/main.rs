use env_logger::Env;

use crate::config::Config;

mod config;
mod daemon;
mod error;
mod message;
mod model;
mod reload;
mod types;

fn main() -> Result<(), error::Error> {
    env_logger::Builder::from_env(Env::default().default_filter_or("info")).init();

    let config = Config::from_env()?;

    let reload_channel = reload::ReloadWatcher::new(config.clone()).watch()?;
    let mut daemon = daemon::Daemon::new(config);

    log::info!("Start daemon");
    daemon.run(reload_channel)?;

    log::info!("Daemon finished, exit");
    Ok(())
}
