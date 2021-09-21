use actix_web::{web, HttpRequest};
use serde::Serialize;

#[derive(Serialize)]
pub struct HealthStatus {
    status: String,
}

pub async fn health(_: HttpRequest) -> web::Json<HealthStatus> {
    web::Json(HealthStatus {
        status: String::from("ok"),
    })
}
