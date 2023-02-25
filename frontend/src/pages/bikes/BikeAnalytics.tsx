import {
  Box,
  Card,
  CardBody,
  CardHeader,
  Container,
  Flex,
  Heading,
  Icon,
  Spinner,
  Stack,
  StackDivider,
  Text,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { SiSimpleanalytics } from 'react-icons/si';

import { API_URL } from '../../../config';

interface BikeAnalyticsProps {
  bikeId: number;
}

interface BikeAnalyticsData {
  totalSales: number;
  unitsSold: number;
  unitsRefunded: number;
}

export default function BikeAnalytics({ bikeId }: BikeAnalyticsProps) {
  const [data, setData] = useState<BikeAnalyticsData>();
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const fetchData = async () => {
    const res = await fetch(`${API_URL}/bikes/${bikeId}/analytics/`);
    const data = await res.json();
    if (!res.ok) {
      setError(data);
    } else {
      setData(data);
    }
    setLoading(false);
  };
  useEffect(() => {
    fetchData();
  }, []);
  return (
    <Card>
      <CardHeader>
        <Flex align="center" gap={2}>
          <Icon as={SiSimpleanalytics} />
          <Heading size="md">Analytics</Heading>
        </Flex>
      </CardHeader>
      <CardBody>
        {loading ? (
          <Spinner />
        ) : (
          <Stack divider={<StackDivider />} spacing={4}>
            <Box>
              <Text>Total Sales: ${data.totalSales.toFixed(0)}</Text>
            </Box>
            <Box>
              <Text>Units Sold: {data.unitsSold}</Text>
            </Box>
            <Box>
              <Text>Units Refunded: {data.unitsRefunded}</Text>
            </Box>
          </Stack>
        )}
        {error && <Container>{error}</Container>}
      </CardBody>
    </Card>
  );
}
