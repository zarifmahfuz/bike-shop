import { Box, Flex, Heading, Spacer } from '@chakra-ui/react';

export default function NavBar() {
  return (
    <Flex as="nav" mb="30px" alignItems="center">
      <Heading as="h2">Bike Shop HQ</Heading>
      <Spacer></Spacer>
      <Box>Admin</Box>
    </Flex>
  );
}
