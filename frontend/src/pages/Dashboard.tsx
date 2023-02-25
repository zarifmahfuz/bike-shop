import { Box } from '@chakra-ui/react';

import AllTimeSales from './analytics/AllTimeSales';
import SalesTrend from './analytics/SalesTrend';
import TopSellingBikes from './analytics/TopSellingBikes';

export default function Dashboard() {
  return (
    <Box>
      <AllTimeSales />

      <SalesTrend />

      <TopSellingBikes />
    </Box>
  );
}
