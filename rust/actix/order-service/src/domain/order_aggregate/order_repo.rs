use async_trait::async_trait;
use std::fmt;
use crate::domain::order_aggregate::order::Order;

#[async_trait]
pub trait OrderRepo {
    async fn create(&self, order: Order) -> Result<Order, ()>;
}