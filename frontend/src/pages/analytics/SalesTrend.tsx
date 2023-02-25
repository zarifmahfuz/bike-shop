import {
  Card,
  CardBody,
  CardHeader,
  Container,
  Flex,
  Heading,
  Icon,
  Spinner,
} from '@chakra-ui/react';
import { useEffect, useState } from 'react';
import { BsGraphUp } from 'react-icons/bs';
import { Line, LineChart, ResponsiveContainer, Tooltip, XAxis, YAxis } from 'recharts';

import { API_URL } from '../../../config';

interface MonthlySale {
  year: number;
  month: number;
  sales: number;
}

const monthNames = [
  'Jan',
  'Feb',
  'Mar',
  'Apr',
  'May',
  'Jun',
  'Jul',
  'Aug',
  'Sep',
  'Oct',
  'Nov',
  'Dec',
];

export default function SalesTrend() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [monthlySales, setMonthlySales] = useState<MonthlySale[]>();
  const fetchData = async () => {
    const res = await fetch(`${API_URL}/analytics/salesTrend/`);
    const data = await res.json();
    if (!res.ok) {
      setError(data);
    } else {
      setMonthlySales(data.reverse());
    }
    setLoading(false);
  };
  useEffect(() => {
    fetchData();
  }, []);

  const formatYAxisTick = (value) => {
    return `${(value / 1000).toFixed(0)}`;
  };
  const formatXAxisTick = (value, index) => {
    const year = monthlySales[index].year.toString().slice(2, 4);
    return `${monthNames[value - 1]} '${year}`;
  };

  const formatTooltipContent = (value) => {
    const formattedValue = `$${value.toLocaleString()}`;
    return <span>{`${formattedValue}`}</span>;
  };
  return (
    <Card bg="gray.50" marginBottom="20px">
      <CardHeader>
        <Flex align="center" gap={2}>
          <Icon as={BsGraphUp} />
          <Heading size="md">Sales Trend</Heading>
        </Flex>
      </CardHeader>
      <CardBody>
        {loading ? (
          <Spinner />
        ) : (
          <ResponsiveContainer width="100%" height={300}>
            <LineChart
              width={1000}
              height={300}
              data={monthlySales}
              margin={{
                top: 5,
                right: 30,
                left: 20,
                bottom: 5,
              }}
            >
              <XAxis
                dataKey="month"
                label={{
                  value: 'Month',
                  position: 'insideBottom',
                  dy: 10,
                  fontSize: 16,
                  fontWeight: 'bold',
                }}
                tickFormatter={formatXAxisTick}
              />
              <YAxis
                label={{
                  value: "Sales ($'000)",
                  angle: -90,
                  position: 'insideLeft',
                  fontSize: 16,
                  fontWeight: 'bold',
                }}
                tickFormatter={formatYAxisTick}
              />
              <Tooltip formatter={formatTooltipContent} />
              <Line
                type="monotone"
                dataKey="sales"
                stroke="#003EAD"
                activeDot={{ r: 8 }}
                dot={true}
              />
            </LineChart>
          </ResponsiveContainer>
        )}
        {error && <Container>{error}</Container>}
      </CardBody>
    </Card>
  );
}
