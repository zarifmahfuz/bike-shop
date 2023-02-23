import {
  Button,
  Card,
  CardBody,
  CardHeader,
  Flex,
  Heading,
  HStack,
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  Spacer,
  Table,
  TableCaption,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
} from '@chakra-ui/react';
import { useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { API_URL } from '../../../config';
import { Sale } from '../../models/sale';

interface BikeSaleInfoCardProps {
  sale: Sale;
}
export default function BikeSaleInfoCard({ sale }: BikeSaleInfoCardProps) {
  const [updateMode, setUpdateMode] = useState(false);
  const [bikeSaleRefunds, setBikeSaleRefunds] = useState({});
  const navigate = useNavigate();
  const processRefund = async () => {
    const refunds = [];
    for (const bikeId in bikeSaleRefunds) {
      // check if the unitsRefunded actually changed
      const bikeSale = sale.bikes.find(
        (bikeSale) => bikeSale.bike.id.toString() === bikeId,
      );
      if (bikeSale.unitsRefunded != bikeSaleRefunds[bikeId]) {
        refunds.push({ id: bikeId, unitsRefunded: bikeSaleRefunds[bikeId] });
      }
    }
    if (refunds.length === 0) {
      return;
    }
    const url = `${API_URL}/sales/${sale.id}/`;
    const res = await fetch(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ refund: refunds }),
    });

    if (res.ok) {
      return navigate(0);
    } else {
      // TODO: Something went wrong
    }
  };
  return (
    <Card>
      <CardHeader>
        <Flex>
          <Heading size="md">Bikes</Heading>
          <Spacer />
          {updateMode ? (
            <HStack>
              <Button size="sm" bg="#85C894" onClick={processRefund}>
                Save
              </Button>
              <Button size="sm" bg="red.400" onClick={() => setUpdateMode(false)}>
                Cancel
              </Button>
            </HStack>
          ) : (
            <Button size="sm" bg="red.400" onClick={() => setUpdateMode(true)}>
              Refund
            </Button>
          )}
        </Flex>
      </CardHeader>
      <CardBody>
        <TableContainer>
          <Table variant="simple">
            <TableCaption>Bikes associated with this sale</TableCaption>
            <Thead>
              <Th>Name / Model</Th>
              <Th>Price ($)</Th>
              <Th>Units Sold</Th>
              <Th>Units Refunded</Th>
            </Thead>
            <Tbody>
              {sale.bikes.map((bikeSale) => (
                <Tr key={bikeSale.bike.id}>
                  <Td>
                    {bikeSale.bike.name} | {bikeSale.bike.model}
                  </Td>
                  <Td>{bikeSale.price}</Td>
                  <Td>{bikeSale.unitsSold}</Td>
                  {updateMode ? (
                    <Td>
                      <NumberInput
                        size="sm"
                        defaultValue={bikeSale.unitsRefunded}
                        min={bikeSale.unitsRefunded}
                        max={bikeSale.unitsSold}
                        onChange={(value) => {
                          const bikeId = bikeSale.bike.id;
                          setBikeSaleRefunds({ ...bikeSaleRefunds, [bikeId]: value });
                        }}
                      >
                        <NumberInputField />
                        <NumberInputStepper>
                          <NumberIncrementStepper />
                          <NumberDecrementStepper />
                        </NumberInputStepper>
                      </NumberInput>
                    </Td>
                  ) : (
                    <Td>{bikeSale.unitsRefunded}</Td>
                  )}
                </Tr>
              ))}
            </Tbody>
          </Table>
        </TableContainer>
      </CardBody>
    </Card>
  );
}
