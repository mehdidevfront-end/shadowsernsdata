import { useState } from 'react';
import Link from 'next/link';
import { useRouter } from 'next/router';
import {
  HomeIcon,
  MapIcon, 
  ShieldCheckIcon,
  UsersIcon,
  DocumentDuplicateIcon,
  EyeIcon,
  BellIcon,
  Cog8ToothIcon,
  TableCellsIcon,
  DocumentTextIcon,
  VideoCameraIcon,
  ChatBubbleLeftRightIcon,
  PresentationChartBarIcon,
  EnvelopeIcon,
  CalendarIcon,
  CloudIcon,
  ArrowLeftOnRectangleIcon
} from '@heroicons/react/24/outline';

const menuItems = [
  { 
    name: "Vue d'ensemble",
    href: '/dashboard',
    icon: HomeIcon 
  },
  { 
    name: 'Cartographie IT',
    href: '/cartography',
    icon: MapIcon 
  },
  { 
    name: 'Détection Shadow IT',
    href: '/shadow-it',
    icon: EyeIcon 
  },
  { 
    name: 'Conformité & Gouvernance',
    href: '/compliance',
    icon: ShieldCheckIcon 
  },
  { 
    name: 'Utilisateurs',
    href: '/users',
    icon: UsersIcon 
  },
  {
    name: 'Google Workspace',
    icon: DocumentDuplicateIcon,
    submenu: [
      { name: 'Google Sheets', href: '/google/sheets', icon: TableCellsIcon },
      { name: 'Google Docs', href: '/google/docs', icon: DocumentTextIcon },
      { name: 'Google Drive', href: '/google/drive', icon: CloudIcon },
      { name: 'Google Meet', href: '/google/meet', icon: VideoCameraIcon },
      { name: 'Google Chat', href: '/google/chat', icon: ChatBubbleLeftRightIcon },
      { name: 'Google Slides', href: '/google/slides', icon: PresentationChartBarIcon },
      { name: 'Emails', href: '/google/emails', icon: EnvelopeIcon },
      { name: 'Events', href: '/google/events', icon: CalendarIcon },
    ]
  }];

const Sidebar = () => {
  const router = useRouter();
  const [collapsed, setCollapsed] = useState(false);

  return (
    <aside className={`bg-gray-800 text-white transition-all duration-300 ${
      collapsed ? 'w-20' : 'w-64'
    } min-h-screen fixed left-0 top-0 z-30`}>
      <div className="p-4 flex items-center justify-between">
        <h1 className={`font-bold text-xl ${collapsed ? 'hidden' : 'block'}`}>
          ShadowGuard
        </h1>
        <button 
          onClick={() => setCollapsed(!collapsed)}
          className="p-1 rounded-lg hover:bg-gray-700"
        >
          <Cog8ToothIcon className="h-6 w-6" />
        </button>
      </div>

      <nav className="mt-8">
        {menuItems.map((item) => {
          const isActive = router.pathname === item.href;
          
          // If item has submenu, render it differently
          if (item.submenu) {
            return (
              <div key={item.name}>
                <div className="flex items-center px-4 py-3 hover:bg-gray-700 transition-colors cursor-pointer">
                  <item.icon className="h-6 w-6 mr-3" />
                  <span className={collapsed ? 'hidden' : 'block'}>
                    {item.name}
                  </span>
                </div>
                {!collapsed && (
                  <div className="pl-8">
                    {item.submenu.map((subItem) => {
                      const isSubItemActive = router.pathname === subItem.href;
                      return (
                        <Link
                          key={subItem.href}
                          href={subItem.href}
                          className={`flex items-center px-4 py-2 text-sm ${
                            isSubItemActive ? 'bg-gray-700' : 'hover:bg-gray-700'
                          } transition-colors`}
                          onClick={(e) => {
                            if (isSubItemActive) {
                              e.preventDefault();
                            }
                          }}
                        >
                          <subItem.icon className="h-5 w-5 mr-2" />
                          <span>{subItem.name}</span>
                        </Link>
                      );
                    })}
                  </div>
                )}
              </div>
            );
          }
          
          // Regular menu item with href
          return (
            <Link
              key={item.href}
              href={item.href}
              className={`flex items-center px-4 py-3 ${
                isActive ? 'bg-gray-700' : 'hover:bg-gray-700'
              } transition-colors`}
              onClick={(e) => {
                if (isActive) {
                  e.preventDefault();
                }
              }}
            >
              <item.icon className="h-6 w-6 mr-3" />
              <span className={collapsed ? 'hidden' : 'block'}>
                {item.name}
              </span>
            </Link>
          );
        })}
      </nav>

      <div className="absolute bottom-0 left-0 right-0 p-4">
        <div className="flex items-center space-x-2">
          <BellIcon className="h-6 w-6" />
          <span className={collapsed ? 'hidden' : 'block'}>
            Notifications
          </span>
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;