import {
  Box,
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
  Stack,
  StackDivider,
  Text,
} from '@chakra-ui/react';
import { useState } from 'react';
import { redirect, useNavigate } from 'react-router-dom';

import { API_URL } from '../../../config';
import { Sale } from '../../models/sale';

interface SaleInfoCardProps {
  sale: Sale;
}

export default function SaleInfoCard({ sale }: SaleInfoCardProps) {
  const [updateMode, setUpdateMode] = useState(false);
  const [discountPercentage, setDiscountPercentage] = useState(sale.discountPercentage);
  const navigate = useNavigate();
  const updateDiscount = async () => {
    const url = `${API_URL}/sales/${sale.id}/`;
    const res = await fetch(url, {
      method: 'PATCH',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ discountPercentage: discountPercentage }),
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
          <Heading size="md">Information</Heading>
          <Spacer />
          {updateMode ? (
            <HStack>
              <Button size="xs" bg="#85C894" onClick={updateDiscount}>
                Save
              </Button>
              <Button size="xs" bg="red.400" onClick={() => setUpdateMode(false)}>
                Cancel
              </Button>
            </HStack>
          ) : (
            <Button size="xs" bg="#85C894" onClick={() => setUpdateMode(true)}>
              Update Discount
            </Button>
          )}
        </Flex>
      </CardHeader>
      <CardBody>
        <Stack divider={<StackDivider />} spacing={4}>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Summary
            </Heading>
            <Flex>
              <Text pt="2" fontSize="sm">
                Date of Sale: {sale.soldAt}
              </Text>
              <Spacer />
              <Text pt="2" fontSize="sm">
                Last Updated: {sale.updatedAt}
              </Text>
            </Flex>

            <Flex>
              <Text pt="2" fontSize="sm">
                Total Sale: ${sale.totalSale}
              </Text>
              <Spacer />
              <Text pt="2" fontSize="sm">
                Applied Discount:{' '}
                {updateMode ? (
                  <NumberInput
                    defaultValue={sale.discountPercentage}
                    min={0}
                    max={100}
                    value={discountPercentage}
                    onChange={(value) => setDiscountPercentage(parseInt(value))}
                    size="sm"
                  >
                    <NumberInputField />
                    <NumberInputStepper>
                      <NumberIncrementStepper />
                      <NumberDecrementStepper />
                    </NumberInputStepper>
                  </NumberInput>
                ) : (
                  <span>{sale.discountPercentage}%</span>
                )}
              </Text>
            </Flex>
            <Text pt="2" fontSize="sm">
              Net Sale: ${sale.netSale}
            </Text>
          </Box>
          <Box>
            <Heading size="xs" textTransform="uppercase">
              Customer
            </Heading>
            <Text pt="2" fontSize="sm">
              Name: {sale.customer.firstName + ' ' + sale.customer.lastName}
            </Text>
            <Text pt="2" fontSize="sm">
              Email: {sale.customer.email}
            </Text>
          </Box>
        </Stack>
      </CardBody>
    </Card>
  );
}
