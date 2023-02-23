import './styles.css';

import { DeleteIcon, SearchIcon } from '@chakra-ui/icons';
import {
  Box,
  Button,
  Flex,
  FormControl,
  FormLabel,
  Heading,
  Input,
  InputGroup,
  InputLeftElement,
  NumberDecrementStepper,
  NumberIncrementStepper,
  NumberInput,
  NumberInputField,
  NumberInputStepper,
  Radio,
  RadioGroup,
  Spacer,
  Stack,
  Table,
  TableContainer,
  Tbody,
  Td,
  Text,
  Tr,
} from '@chakra-ui/react';
import { SetStateAction, useEffect, useState } from 'react';
import { Form, redirect, useActionData } from 'react-router-dom';

import { API_URL } from '../../../config';
import ErrorBanner from '../../components/ErrorBanner';
import { Bike } from '../../models/bike';
import useDebounce from '../../utils';

export default function CreateSale() {
  const data = useActionData();
  const [searchInput, setSearchInput] = useState('');
  const [bikes, setBikes] = useState<Bike[]>([]);
  const [bikesSelected, setBikesSelected] = useState<Bike[]>([]);

  const fetchBikes = async () => {
    if (searchInput.length == 0) {
      return;
    }
    const url = `${API_URL}/bikes?search=${searchInput}`;
    const res = await fetch(url);
    const data = await res.json();
    if (res.ok) {
      setBikes(data.filter((bike) => bike.unitsAvailable > 0).slice(0, 5));
    }
  };

  useEffect(() => {
    if (searchInput.length == 0) {
      setBikes([]);
    }
  }, [searchInput]);

  useDebounce(fetchBikes, [searchInput], 300);

  const handleSearchInputChange = (input: {
    preventDefault: () => void;
    target: { value: SetStateAction<string> };
  }) => {
    input.preventDefault();
    setSearchInput(input.target.value);
  };

  return (
    <>
      <Heading as="h3" size="lg">
        New Sale
      </Heading>
      <Box maxW="700px">
        <Form method="post" action="">
          <Box margin="15px">
            <Heading as="h4" size="md">
              Bikes
            </Heading>

            <Box marginY="15px">
              <InputGroup>
                <InputLeftElement pointerEvents="none">
                  <SearchIcon color="gray.300" />
                </InputLeftElement>
                <Input
                  type="search"
                  placeholder="Search for bikes"
                  value={searchInput}
                  onChange={handleSearchInputChange}
                />
              </InputGroup>

              {bikes && (
                <TableContainer>
                  <Table variant="simple">
                    <Tbody>
                      {bikes.map((bike) => (
                        <Tr key={bike.id}>
                          <Td>
                            <Flex alignItems="center">
                              <Text>
                                {bike.name} - {bike.model}
                              </Text>
                              <Spacer />
                              <Button
                                bg="green.400"
                                onClick={() => {
                                  setSearchInput('');
                                  for (const b of bikesSelected) {
                                    if (bike.id == b.id) {
                                      return;
                                    }
                                  }
                                  setBikesSelected([...bikesSelected, bike]);
                                }}
                              >
                                Select
                              </Button>
                            </Flex>
                          </Td>
                        </Tr>
                      ))}
                    </Tbody>
                  </Table>
                </TableContainer>
              )}
            </Box>

            {bikesSelected &&
              bikesSelected.map((selectedBike) => (
                <FormControl isRequired m="10px" key={selectedBike.id}>
                  <Flex alignItems="center" gap={2}>
                    <FormLabel>
                      {selectedBike.name} | {selectedBike.model} (${selectedBike.price})
                    </FormLabel>
                    <Spacer />
                    <NumberInput
                      size="md"
                      defaultValue={1}
                      min={1}
                      max={selectedBike.unitsAvailable}
                      maxW={24}
                    >
                      <NumberInputField name={`bike/${selectedBike.id}`} />
                      <NumberInputStepper>
                        <NumberIncrementStepper />
                        <NumberDecrementStepper />
                      </NumberInputStepper>
                    </NumberInput>
                    <Button
                      leftIcon={<DeleteIcon />}
                      bg="red.400"
                      iconSpacing="0"
                      onClick={() => {
                        setBikesSelected(
                          bikesSelected.filter((b) => b.id != selectedBike.id),
                        );
                      }}
                    />
                  </Flex>
                </FormControl>
              ))}

            <Heading as="h4" size="md">
              Customer Information
            </Heading>

            <FormControl isRequired m="10px">
              <Flex alignItems="center" gap={2}>
                <FormLabel>Email:</FormLabel>
                <Spacer />
                <Input
                  placeholder="mahfuz.zarif@gmail.com"
                  name="email"
                  size="md"
                  type="email"
                />
              </Flex>
            </FormControl>

            <FormControl isRequired m="10px">
              <Flex alignItems="center" gap={2}>
                <FormLabel>First Name:</FormLabel>
                <Input placeholder="Zarif" name="firstName" size="md" maxWidth={300} />
              </Flex>
            </FormControl>

            <FormControl isRequired m="10px">
              <Flex alignItems="center" gap={2}>
                <FormLabel>Last Name:</FormLabel>
                <Input placeholder="Mahfuz" name="lastName" size="md" maxWidth={300} />
              </Flex>
            </FormControl>

            <Heading as="h4" size="md">
              Other Information
            </Heading>

            <FormControl isRequired m="10px">
              <Flex alignItems="center" gap={2}>
                <FormLabel>Date of Sale</FormLabel>
                <Input name="date" type="date" maxW={250} />
              </Flex>
            </FormControl>

            <FormControl isRequired m="10px">
              <Flex alignItems="center" gap={2}>
                <FormLabel>Discount Applied (%)</FormLabel>
                <NumberInput defaultValue={0} min={0} max={100} maxW={24} precision={0}>
                  <NumberInputField name="discountPercentage" />
                </NumberInput>
              </Flex>
            </FormControl>

            <FormControl isRequired m="10px">
              <Flex gap={2}>
                <FormLabel>Payment Method:</FormLabel>
                <RadioGroup name="paymentMethod">
                  <Stack spacing={4} direction="row">
                    <Radio value="credit/debit">Credit/Debit</Radio>
                    <Radio value="cash">Cash</Radio>
                  </Stack>
                </RadioGroup>
              </Flex>
            </FormControl>

            <Button type="submit" bg="green.400" m="10px">
              Submit
            </Button>
          </Box>

          {data && <ErrorBanner error={data['error'] as string | undefined} />}
        </Form>

        {/* <div className="sales-summary">
          <div>Total Sale: ${totalSale}</div>
          <div>Discount Applied: ${discountPercentage}</div>
          <hr />
          <div>Net Sale: ${netSale}</div>
        </div> */}
      </Box>
    </>
  );
}

export const createSaleAction = async ({ request }) => {
  const data = await request.formData();
  const bikes = [];
  for (const key of data.keys()) {
    if (key.includes('bike')) {
      bikes.push({
        id: parseInt(key.split('/')[1]),
        unitsSold: data.get(key),
      });
    }
  }
  if (bikes.length === 0) {
    return { error: 'You must select at least one bike' };
  }
  const submission = {
    bikes: bikes,
    customer: {
      email: data.get('email'),
      firstName: data.get('firstName'),
      lastName: data.get('lastName'),
    },
    paymentMethod: data.get('paymentMethod'),
    date: data.get('date'),
    discountPercentage: data.get('discountPercentage'),
  };
  console.log('Submission: ', submission);

  const res = await fetch(`${API_URL}/sales/`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(submission),
  });
  const resData = await res.json();
  if (!res.ok) {
    return { error: resData.error[0].message };
  }
  return redirect('/sales');
};
