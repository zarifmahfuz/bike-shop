import { BikeSale } from './bikeSale';
import { Customer } from './customer';

export interface Sale {
  id: number;
  totalSale: number;
  netSale: number;
  discountPercentage: number;
  soldAt: string;
  updatedAt: string;
  customer: Customer;
  bikes: BikeSale[];
}
