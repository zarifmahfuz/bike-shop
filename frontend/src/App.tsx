import {
  createBrowserRouter,
  createRoutesFromElements,
  Route,
  RouterProvider,
} from 'react-router-dom';

import RootLayout from './layouts/RootLayout';
import AddBike, { createBikeAction } from './pages/bikes/AddBike';
import BikeDetails, { bikeDetailsLoader } from './pages/bikes/BikeDetails';
import Bikes from './pages/bikes/Bikes';
import EditBike, { editBikeAction } from './pages/bikes/EditBike';
import Dashboard from './pages/Dashboard';
import CreateSale, { createSaleAction } from './pages/sales/CreateSale';
import SaleDetails, { saleDetailsLoader } from './pages/sales/SaleDetails';
import Sales from './pages/sales/Sales';

// router and routes
const router = createBrowserRouter(
  createRoutesFromElements(
    <Route path="/" element={<RootLayout />}>
      <Route index element={<Dashboard />} />

      <Route path="bikes">
        <Route index element={<Bikes />} />
        <Route path="new" element={<AddBike />} action={createBikeAction} />
        <Route path=":id">
          <Route index element={<BikeDetails />} loader={bikeDetailsLoader} />
          <Route
            path="edit"
            element={<EditBike />}
            loader={bikeDetailsLoader}
            action={editBikeAction}
          />
        </Route>
      </Route>

      <Route path="sales">
        <Route index element={<Sales />} />
        <Route path="new" element={<CreateSale />} action={createSaleAction} />
        <Route path=":id" element={<SaleDetails />} loader={saleDetailsLoader} />
      </Route>
    </Route>,
  ),
);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
