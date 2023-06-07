use chrono::Timelike;
use sqlite;
use std::{env::args,  path::PathBuf};
const DATABASE: &str = "/home/aura/Venvs/rustVenv/backup_rs/backupdatabase.db";
const TESTDATE: &str = "2023-12-01 12:45:36";
const TESTPATH: &str = "/home/aura/Venvs/rustVenv/backup_rs/";

struct  FileEntry {
    path: String,
    date: String
}


fn main() {
   //Colect args

    let pwd = std::env::current_dir();
    let mut args: Vec<String> = args().collect();
    //If  aggs less then 1
    if args.len() == 1 {
        help();
        std::process::exit(1);
    }
    // get user input
    let user_input = String::from(&args[1]);
    //remove unused variables
    args.splice(0..1, std::iter::empty());
    // Match and applai correct heplp
    match user_input.as_str() {
        "-addP" => add_to_db(TESTPATH, true).unwrap(),
        "-addC" => add_to_db(TESTPATH, false).unwrap(),
        "-d" => open_daschboard(),
        "-h" => {
            help();
            std::process::exit(0)

        }

        _ => {
            println!("wrong argument ");
            help();
            std::process::exit(1)
        }
    }
}
//
//Add Paths and time potrnily maby just collect the vector and nothing more
fn add_path_time(paths: &Vec<String>) -> Vec<String> {
    let path_bufs: Vec<PathBuf> = paths.iter().map(|i| PathBuf::from(i)).collect();
    let mut valid_paths: Vec<String> = Vec::new();
    let pwd = std::env::current_dir();

    for i in path_bufs {
        if i.exists() {
            //Add the path to the itreator i iterator 
            valid_paths.push(i.to_str().unwrap().to_string());
        } else {
            eprintln!("Skipping: This is not a valid path: {:?}", i);
        }
    }


    valid_paths
}

fn add_to_db(vector_of_paths: &str, decison: bool) -> Result<(), sqlite::Error> {
    // Sqlite docs (https://docs.rs/sqlite/latest/sqlite/)
    let mut query = String::new();
    let time = chrono::prelude::Local::now();
   let date = format!("{} {}:{}",time.date_naive(),time.hour(),time.minute());
    if decison {
        query = format!(
            "INSERT INTO Continous (path,date) VALUES ('{}',{} );",
            vector_of_paths,date
        );
    } else {
        query = format!(
            "INSERT INTO Temporary (path,date) VALUES ('{}','{}' );",
            vector_of_paths,date
        );
    }
    if query == "" {
        eprintln!("No query provided");
        std::process::exit(1)
    } else {
        let connection = sqlite::open(&DATABASE)?;
        connection.execute(&query)?;
        Ok(())
    }
}

fn open_daschboard() {
    println!("Im opening daschboard")
}

fn help() {
    println!(
        "
This is help
-d open daschboard 
-addP add permanetly 
-addT add temporerly 

--r remove from the list  
"
    )
}
