import {
  Box,
  Button,
  FormControl,
  FormLabel,
  HStack,
  Input,
  NumberInput,
  NumberInputField,
  Textarea,
} from '@chakra-ui/react';
import { Form, useActionData, useNavigate } from 'react-router-dom';

import ErrorBanner from '../../components/ErrorBanner';
import { Bike } from '../../models/bike';

interface BikeFormProps {
  action: string;
  bike?: Bike;
}

export default function BikeForm({ action, bike }: BikeFormProps) {
  const data = useActionData();
  const navigate = useNavigate();
  return (
    <Box maxW="480px">
      <Form method="post" action={action}>
        <FormControl isRequired m="10px">
          <FormLabel>Name</FormLabel>
          <Input
            type="text"
            name="name"
            placeholder="Trek Marlin"
            defaultValue={bike?.name}
          ></Input>
        </FormControl>

        <FormControl isRequired m="10px">
          <FormLabel>Model</FormLabel>
          <Input
            type="text"
            name="model"
            placeholder="Trek Marlin 6"
            defaultValue={bike?.model}
          ></Input>
        </FormControl>

        <FormControl isRequired m="10px">
          <FormLabel>Price</FormLabel>
          <NumberInput precision={2} defaultValue={bike?.price}>
            <NumberInputField name="price" placeholder="1049.99" />
          </NumberInput>
        </FormControl>

        <FormControl isRequired m="10px">
          <FormLabel>Units Available</FormLabel>
          <NumberInput precision={0} min={0} defaultValue={bike?.unitsAvailable}>
            <NumberInputField name="unitsAvailable" placeholder="10" />
          </NumberInput>
        </FormControl>

        <FormControl m="10px">
          <FormLabel>Description</FormLabel>
          <Textarea
            placeholder="Enter a short description about the bike!"
            name="description"
            defaultValue={bike?.description}
          />
        </FormControl>

        <FormControl m="10px">
          <FormLabel>Image link</FormLabel>
          <Input
            type="url"
            name="image"
            placeholder="https://images.unsplash.com/photo-1501147830916-ce44a6359892?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=1470&q=80"
            defaultValue={bike?.image}
          ></Input>
        </FormControl>

        {bike ? (
          <HStack spacing={4}>
            <Button type="submit" color="white" bg="green.400" m="10px">
              Save
            </Button>
            <Button color="white" bg="red.400" m="10px" onClick={() => navigate(-1)}>
              Cancel
            </Button>
          </HStack>
        ) : (
          <Button type="submit" colorScheme="green" m="10px">
            Submit
          </Button>
        )}

        {data && <ErrorBanner error={data.error as string | undefined} />}
      </Form>
    </Box>
  );
}
