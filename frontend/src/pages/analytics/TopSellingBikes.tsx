import {
  Card,
  CardBody,
  CardHeader,
  Container,
  Heading,
  Spinner,
  Table,
  TableCaption,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';

import { API_URL } from '../../../config';
import { Bike } from '../../models/bike';

interface BikeSaleData {
  bike: Bike;
  sales: number;
  percentageTotalSales: number;
}

export default function TopSellingBikes() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [topBikes, setTopBikes] = useState<BikeSaleData[]>();
  const fetchData = async () => {
    const res = await fetch(`${API_URL}/analytics/topSellingBikes/`);
    const data = await res.json();
    if (!res.ok) {
      setError(data);
    } else {
      setTopBikes(data.slice(0, 5));
    }
    setLoading(false);
  };
  useEffect(() => {
    fetchData();
  }, []);
  return (
    <Card bg="gray.50" maxWidth="700px">
      <CardHeader>
        <Heading size="md">Top Selling Bikes</Heading>
      </CardHeader>
      <CardBody>
        {loading ? (
          <Spinner />
        ) : (
          <TableContainer>
            <Table variant="simple">
              <TableCaption>Only top five are shown</TableCaption>
              <Thead>
                <Tr>
                  <Th>#</Th>
                  <Th>Bike</Th>
                  <Th>Sales (%)</Th>
                  <Th>Sales ($)</Th>
                </Tr>
              </Thead>
              <Tbody>
                {topBikes.map((bike, index) => (
                  <Tr key={bike.bike.id}>
                    <Td>{index + 1}</Td>
                    <Td>
                      {bike.bike.name} | {bike.bike.model}
                    </Td>
                    <Td>{bike.percentageTotalSales.toFixed(0)}</Td>
                    <Td>{bike.sales}</Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          </TableContainer>
        )}
        {error && <Container>{error}</Container>}
      </CardBody>
    </Card>
  );
}
