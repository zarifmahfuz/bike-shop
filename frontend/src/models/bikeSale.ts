import { Bike } from './bike';

export interface BikeSale {
  bike: Bike;
  unitsSold: number;
  unitsRefunded: number;
  price: number;
}
