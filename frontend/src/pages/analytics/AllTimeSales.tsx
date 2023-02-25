import {
  Card,
  CardBody,
  CardHeader,
  Container,
  Flex,
  Heading,
  SimpleGrid,
  Spinner,
  Text,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';

import { API_URL } from '../../../config';

interface AllTimeSalesData {
  totalSales: number;
  totalDiscount: number;
  bikesSold: number;
  bikesRefunded: number;
}

export default function AllTimeSales() {
  const [allTimeSalesData, setAllTimeSalesData] = useState<AllTimeSalesData>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const fetchData = async () => {
    const res = await fetch(`${API_URL}/analytics/allTimeSales/`);
    const data = await res.json();
    if (!res.ok) {
      setError(data);
    } else {
      setAllTimeSalesData(data);
    }
    setLoading(false);
  };
  useEffect(() => {
    fetchData();
  }, []);
  return (
    <Card bg="gray.50" marginBottom="20px">
      <CardHeader>
        <Heading size="md">All Time Sales</Heading>
      </CardHeader>
      <CardBody>
        {loading ? (
          <Spinner />
        ) : (
          <SimpleGrid spacing={4} templateColumns="repeat(auto-fill, minmax(200px, 1fr))">
            <Card bg="gray.50">
              <CardHeader pb="0">
                <Flex alignItems="center" gap="10px" justify="space-around">
                  <Heading size="md">Total Sales</Heading>
                </Flex>
              </CardHeader>
              <CardBody fontSize="2xl">
                <Flex justify="space-around">
                  <Text as="b">${allTimeSalesData.totalSales.toFixed(0)}</Text>
                </Flex>
              </CardBody>
            </Card>
            <Card bg="gray.50">
              <CardHeader pb="0">
                <Flex alignItems="center" gap="10px" justify="space-around">
                  <Heading size="md">Total Discount</Heading>
                </Flex>
              </CardHeader>
              <CardBody fontSize="2xl">
                <Flex justify="space-around">
                  <Text as="b">${allTimeSalesData.totalDiscount.toFixed(0)}</Text>
                </Flex>
              </CardBody>
            </Card>
            <Card bg="gray.50">
              <CardHeader pb="0">
                <Flex alignItems="center" gap="10px" justify="space-around">
                  <Heading size="md">Bikes Sold</Heading>
                </Flex>
              </CardHeader>
              <CardBody fontSize="2xl">
                <Flex justify="space-around">
                  <Text as="b">{allTimeSalesData.bikesSold}</Text>
                </Flex>
              </CardBody>
            </Card>
            <Card bg="gray.50">
              <CardHeader pb="0">
                <Flex alignItems="center" gap="10px" justify="space-around">
                  <Heading size="md">Bikes Refunded</Heading>
                </Flex>
              </CardHeader>
              <CardBody fontSize="2xl">
                <Flex justify="space-around">
                  <Text as="b">{allTimeSalesData.bikesRefunded}</Text>
                </Flex>
              </CardBody>
            </Card>
          </SimpleGrid>
        )}
        {error && <Container>{error}</Container>}
      </CardBody>
    </Card>
  );
}
