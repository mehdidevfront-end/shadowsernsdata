import { BellIcon, UserCircleIcon } from '@heroicons/react/24/outline';

const Topbar = () => {
  const notifications = [
    { id: 1, text: 'Nouveau shadow IT détecté', date: '2min' },
    { id: 2, text: 'Rapport hebdomadaire disponible', date: '1h' },
  ];

  return (
    <div className="fixed top-0 right-0 left-64 h-16 bg-white border-b z-20 flex items-center justify-between px-6">
      <div className="flex-1">
        <div className="relative max-w-md">
          <input
            type="search"
            placeholder="Rechercher..."
            className="w-full px-4 py-2 border rounded-lg"
          />
        </div>
      </div>

      <div className="flex items-center space-x-4">
        <div className="relative">
          <button className="relative p-2 rounded-full hover:bg-gray-100">
            <BellIcon className="h-6 w-6" />
            <span className="absolute top-0 right-0 h-4 w-4 bg-red-500 rounded-full text-xs text-white flex items-center justify-center">
              2
            </span>
          </button>

          <div className="absolute right-0 mt-2 w-80 bg-white rounded-lg shadow-lg border hidden group-hover:block">
            <div className="p-4">
              <h3 className="font-semibold mb-2">Notifications</h3>
              {notifications.map(notif => (
                <div key={notif.id} className="py-2 border-b last:border-0">
                  <p className="text-sm">{notif.text}</p>
                  <span className="text-xs text-gray-500">{notif.date}</span>
                </div>
              ))}
            </div>
          </div>
        </div>

        <button className="flex items-center space-x-2 p-2 rounded-lg hover:bg-gray-100">
          <UserCircleIcon className="h-8 w-8" />
          <div className="text-left">
            <p className="text-sm font-medium">John Doe</p>
            <p className="text-xs text-gray-500">Administrateur</p>
          </div>
        </button>
      </div>
    </div>
  );
};

export default Topbar;