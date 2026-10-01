from pydantic import BaseModel, Field


class ReceiptOrder(BaseModel):
    order_id: str
    quantity: int
    status: str
    order_date: str


class ReceiptCustomerAddress(BaseModel):
    city: str
    state: str
    country: str


class ReceiptCustomer(BaseModel):
    user_id: str
    name: str
    email: str
    phone: str
    address: ReceiptCustomerAddress


class ReceiptProduct(BaseModel):
    product_id: str
    name: str
    category: str
    brand: str
    price: float


class ReceiptInvoice(BaseModel):
    invoice_id: str
    subtotal: float
    tax: float
    discount: float
    shipping: float
    total: float
    payment_status: str


class ReceiptResponse(BaseModel):
    """Aggregated order receipt response combining four MongoDB collections."""

    order: ReceiptOrder
    customer: ReceiptCustomer
    product: ReceiptProduct
    invoice: ReceiptInvoice
