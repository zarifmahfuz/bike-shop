import { Bike } from './bike';

export interface BikeSale {
  bike: Bike;
  unitsSold: number;
  unitsRefund: number;
  price: number;
}
