# from fastapi import HTTPException

# from app.models.groups import Product
# from app.models.tickets import CostCenter
# from app.repository.products.product_sales_reposiroty import ProductSalesRepository

# class ProductSalesService:


#     @staticmethod
#     def get_product_sales(self, db, product_id: int, cost_center_id: int, period_days: int = 30):
#         if period_days <= 0:
#             raise HTTPException(status_code=400, detail="Period must be positive")
        
#         product = db.query(Product).get(product_id)
#         if not product:
#             raise HTTPException(status_code=404, detail="Product not found")
            
#         cost_center = db.query(CostCenter).get(cost_center_id)
#         if not cost_center:
#             raise HTTPException(status_code=404, detail="Cost center not found")

#         return self.sales_repo.get_product_sales(db, product_id, cost_center_id, period_days)