import '../styles.css';

import { AddIcon, SearchIcon } from '@chakra-ui/icons';
import {
  Box,
  Button,
  Card,
  CardBody,
  CardHeader,
  Container,
  Divider,
  Flex,
  Heading,
  HStack,
  Image,
  Input,
  InputGroup,
  InputLeftElement,
  SimpleGrid,
  Spacer,
  Stack,
  Text,
} from '@chakra-ui/react';
import { SetStateAction, useState } from 'react';
import { useNavigate } from 'react-router-dom';

import { API_URL } from '../../../config';
import { Bike } from '../../models/bike';
import useDebounce from '../../utils';

export default function Bikes() {
  // TODO: Add a 'total sales' field
  const [bikes, setBikes] = useState<Bike[]>([]);
  const [error, setError] = useState('');
  const [searchInput, setSearchInput] = useState('');

  const fetchBikes = async () => {
    let url = `${API_URL}/bikes`;
    if (searchInput.length > 0) {
      url += `?search=${searchInput}`;
    }
    const res = await fetch(url);
    const data = await res.json();
    if (res.ok) {
      setBikes(data);
    } else {
      setError(data);
    }
  };

  useDebounce(fetchBikes, [searchInput], 300);

  const handleSearchInputChange = (input: {
    preventDefault: () => void;
    target: { value: SetStateAction<string> };
  }) => {
    input.preventDefault();
    setSearchInput(input.target.value);
  };

  const navigate = useNavigate();

  return (
    <>
      <HStack marginY="15px">
        <InputGroup>
          <InputLeftElement pointerEvents="none">
            <SearchIcon color="gray.300" />
          </InputLeftElement>
          <Input
            type="search"
            placeholder="Search for bikes by name/model"
            onChange={handleSearchInputChange}
            value={searchInput}
          />
        </InputGroup>
        <Button
          bg="#85C894"
          leftIcon={<AddIcon />}
          onClick={() => navigate('/bikes/new')}
        >
          Add Bike
        </Button>
      </HStack>
      <SimpleGrid spacing={10} minChildWidth="300px">
        {bikes &&
          bikes.map((bike) => (
            <Card
              key={bike.id}
              bg="white"
              onClick={() => navigate(bike.id.toString())}
              className="clickable"
            >
              <CardHeader pb="0">
                <Heading as="h3" size="sm">
                  {bike.model} | {bike.name}
                </Heading>
              </CardHeader>
              <CardBody>
                <Image src={bike.image} alt="Image not available" borderRadius="md" />
                <Stack mt="6" spacing="3">
                  <Flex>
                    <Text marginX="20px">${bike.price}</Text>
                    <Spacer></Spacer>
                    <Text marginX="20px">Units Available: {bike.unitsAvailable}</Text>
                  </Flex>
                  <Box color="gray.500">
                    <Text noOfLines={6}>{bike.description}</Text>
                  </Box>
                </Stack>
              </CardBody>
            </Card>
          ))}
      </SimpleGrid>
      {error && <Container>{error}</Container>}
    </>
  );
}
