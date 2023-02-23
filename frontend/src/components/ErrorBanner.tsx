import {
  Alert,
  AlertDescription,
  AlertIcon,
  AlertTitle,
  Box,
  CloseButton,
  useDisclosure,
} from '@chakra-ui/react';

interface RequestError {
  error: string | undefined;
}

export default function ErrorBanner({ error }: RequestError) {
  if (!error) {
    return;
  }
  const { isOpen: isVisible, onClose, onOpen } = useDisclosure({ defaultIsOpen: true });
  return (
    <Alert status="error" m="10px">
      <AlertIcon />
      <Box>
        <AlertTitle>Error</AlertTitle>
        <AlertDescription>{error}</AlertDescription>
      </Box>
      {/* <CloseButton
        alignSelf="flex-start"
        position="relative"
        right={-1}
        top={-1}
        onClick={onClose}
      /> */}
    </Alert>
  );
}
