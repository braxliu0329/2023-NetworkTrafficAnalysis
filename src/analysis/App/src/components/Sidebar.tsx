import React from 'react';
import { Link } from 'react-router-dom';

export interface Page {
  title: string;
  path: string;
  children?: Page[];
}

interface SidebarProps {
  pages: Page[];
}

const Sidebar: React.FC<SidebarProps> = ({ pages }) => {
  return (
    <nav className="sidebar">
      <ul>
        {pages.map((page, index) => (
          <li key={index}>
            <Link to={page.path}>{page.title}</Link>
            {page.children && (
              <ul>
                {page.children.map((child, childIndex) => (
                  <li key={childIndex}>
                    <Link to={child.path}>{child.title}</Link>
                  </li>
                ))}
              </ul>
            )}
          </li>
        ))}
      </ul>
    </nav>
  );
};

export default Sidebar;

