
use fs_extra::dir;
use std::path::{Path, PathBuf};
use std::fs;

const DATABASE: &str = "/home/dnf/eNV/rustVenvs/backup/backup.db";

fn main() {
    let paths = execute_query().unwrap();
    println!("{:?}", paths);

    let home_dir = dirs::home_dir().expect("Failed to get home directory");
    let encryp_backup = home_dir.join(".encrypted_backup");
    
    if !encryp_backup.exists() {
        fs::create_dir(&encryp_backup).expect("Failed to create directory");
    } else {
        println!("It already exists.");
    }
    
    copy_files(&paths, &encryp_backup.to_string_lossy());
}

fn execute_query() -> Result<Vec<String>, Box<dyn std::error::Error>> {
    let mut paths: Vec<String> = Vec::new();
    let connection = sqlite::open(&DATABASE)?;
    let query = "SELECT path FROM Temporary;";
    
    for row in connection.prepare(query)?.into_iter().map(|row| row.unwrap()) {
        let path: String = row.read::<&str,_>("path").to_string();
        paths.push(path);
    }
    
    Ok(paths)
}


fn copy_files(paths: &[String], backup_dir: &str) {
    let options = dir::CopyOptions::new();
    
    for entry in paths {
        let source = Path::new(entry);
        let destination = PathBuf::from(backup_dir).join(source.file_name().unwrap());

        if source.is_dir() {
            if let Err(e) = dir::copy(source, &destination, &options) {
                eprintln!("Error copying directory {:?}: {}", source, e);
            }
        } else {
            if let Err(e) = fs::copy(source, &destination) {
                eprintln!("Error copying file {:?}: {}", source, e);
            }
        }
        
        println!("Copied {:?} to {:?}", source, destination);
    }
}
