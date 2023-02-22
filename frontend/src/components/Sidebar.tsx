import { List, ListIcon, ListItem } from '@chakra-ui/react';
import { IoMdAnalytics } from 'react-icons/io';
import { MdAttachMoney, MdDirectionsBike } from 'react-icons/md';
import { NavLink } from 'react-router-dom';

export default function Sidebar() {
  return (
    <List fontSize="1.2em" spacing={4} padding="10px" margin="10px">
      <ListItem>
        <ListIcon as={IoMdAnalytics} />
        <NavLink to="/">Dashboard</NavLink>
      </ListItem>
      <ListItem>
        <ListIcon as={MdDirectionsBike} />
        <NavLink to="/bikes">Bikes</NavLink>
      </ListItem>
      <ListItem>
        <ListIcon as={MdAttachMoney} />
        <NavLink to="/sales">Sales</NavLink>
      </ListItem>
    </List>
  );
}
