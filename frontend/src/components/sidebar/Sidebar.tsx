import { useState } from 'react';
import { Sidebar, Menu, MenuItem } from 'react-pro-sidebar';
import {Button} from 'react-bootstrap';
// import { IoIosHome } from "react-icons/io";
import { IoNewspaper } from "react-icons/io5";
import { RxHamburgerMenu } from "react-icons/rx";
import "./Sidebar.scss";


const SidebarNav = () => {
    const [collapsed, setCollapsed] = useState(true);

  return (
    <Sidebar data-bs-theme="dark" style={{height: "100%"}} collapsed={collapsed} transitionDuration={100} breakPoint='md'>
        <div className='sidebar-header d-flex justify-content-center mb-3'>
            <Button variant="dark" onClick={() => setCollapsed(!collapsed)}>{<RxHamburgerMenu/>}</Button>
        </div>
        <Menu>
            {/* <MenuItem>{<IoIosHome/>} Home</MenuItem> */}
            <MenuItem>{<IoNewspaper/>} Predict</MenuItem>
        </Menu>
          

    </Sidebar>

  )
};

export default SidebarNav;
