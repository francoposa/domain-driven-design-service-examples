mod application;
mod domain;

use actix_web::{web, App, HttpServer};

#[actix_web::main]
async fn main() -> std::io::Result<()> {
    let app = || {
        App::new().route(
            "/health",
            web::get().to(application::server::health_handler::health),
        )
    };
    let server = HttpServer::new(app)
        .bind("127.0.0.1:8080")
        .expect("failed to bind on 127.0.0.1:8080");

    println!("running http server on 127.0.0.1:8080...");
    server.run().await
}
