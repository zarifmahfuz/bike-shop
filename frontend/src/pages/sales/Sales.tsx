import '../styles.css';

import { AddIcon, SearchIcon, TriangleDownIcon, TriangleUpIcon } from '@chakra-ui/icons';
import {
  Box,
  Button,
  Container,
  HStack,
  Input,
  InputGroup,
  InputLeftElement,
  ListItem,
  Popover,
  PopoverArrow,
  PopoverBody,
  PopoverContent,
  PopoverTrigger,
  Radio,
  RadioGroup,
  Stack,
  Table,
  TableCaption,
  TableContainer,
  Tbody,
  Td,
  Th,
  Thead,
  Tr,
  UnorderedList,
  useDisclosure,
} from '@chakra-ui/react';
import { SetStateAction, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { API_URL } from '../../../config';
import { Sale } from '../../models/sale';
import useDebounce from '../../utils';

export default function Sales() {
  const { isOpen, onToggle, onClose } = useDisclosure();
  const navigate = useNavigate();
  const [filterValue, setFilterValue] = useState('email');
  const [sales, setSales] = useState<Sale[]>([]);
  const [error, setError] = useState('');
  const [searchInput, setSearchInput] = useState('');

  const fetchSales = async () => {
    let url = `${API_URL}/sales/`;
    if (searchInput.length > 0) {
      if (filterValue === 'email') {
        url += `?email=${searchInput}`;
      } else {
        url += `?bike=${searchInput}`;
      }
    }
    const res = await fetch(url);
    const data = await res.json();
    if (res.ok) {
      setSales(data);
    } else {
      setError(data);
    }
  };

  useDebounce(fetchSales, [searchInput, filterValue], 300);

  const handleSearchInputChange = (input: {
    preventDefault: () => void;
    target: { value: SetStateAction<string> };
  }) => {
    input.preventDefault();
    setSearchInput(input.target.value);
  };
  return (
    <Box>
      <HStack>
        <InputGroup>
          <InputLeftElement pointerEvents="none">
            <SearchIcon color="gray.300" />
          </InputLeftElement>
          <Input
            type="search"
            placeholder="Search"
            onChange={handleSearchInputChange}
            value={searchInput}
          />
        </InputGroup>

        <Popover onClose={onClose}>
          <PopoverTrigger>
            <Button
              onClick={onToggle}
              bg="#85C894"
              rightIcon={isOpen ? <TriangleUpIcon /> : <TriangleDownIcon />}
            >
              Filter
            </Button>
          </PopoverTrigger>
          <PopoverContent>
            <PopoverArrow />
            <PopoverBody>
              <RadioGroup onChange={setFilterValue} value={filterValue}>
                <Stack>
                  <Radio value="email">Customer Email</Radio>
                  <Radio value="bike">Bike Name/Model</Radio>
                </Stack>
              </RadioGroup>
            </PopoverBody>
          </PopoverContent>
        </Popover>

        <Button leftIcon={<AddIcon />} onClick={() => navigate('new')} bg="#85C894">
          New Sale
        </Button>
      </HStack>

      <TableContainer>
        <Table variant="simple">
          <TableCaption>Bike Sales</TableCaption>
          <Thead>
            <Tr>
              <Th>Date</Th>
              <Th>Net Sale ($)</Th>
              <Th>Discount (%)</Th>
              <Th>Customer</Th>
              <Th>Total Bikes Sold</Th>
              <Th>Total Bikes Refunded</Th>
              <Th>Bikes</Th>
            </Tr>
          </Thead>
          <Tbody>
            {sales &&
              sales.map((sale) => (
                <Tr
                  key={sale.id}
                  onClick={() => navigate(`${sale.id}`)}
                  className="clickable"
                >
                  <Td>{sale.soldAt}</Td>
                  <Td>{sale.netSale}</Td>
                  <Td>{sale.discountPercentage}</Td>
                  <Td>{sale.customer.email}</Td>
                  <Td>
                    {sale.bikes.reduce(
                      (totalBikesSold, bikeSale) => totalBikesSold + bikeSale.unitsSold,
                      0,
                    )}
                  </Td>
                  <Td>
                    {sale.bikes.reduce(
                      (totalBikesRefunded, bikeSale) =>
                        totalBikesRefunded + bikeSale.unitsRefunded,
                      0,
                    )}
                  </Td>
                  <Td>
                    <UnorderedList>
                      {sale.bikes.map((bikeSale) => (
                        <ListItem key={bikeSale.bike.id}>
                          {bikeSale.bike.name} | {bikeSale.bike.model}
                        </ListItem>
                      ))}
                    </UnorderedList>
                  </Td>
                </Tr>
              ))}
          </Tbody>
        </Table>
      </TableContainer>

      {error && <Container>{error}</Container>}
    </Box>
  );
}
