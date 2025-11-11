import React, { useState } from 'react';
import DataTable from '@/components/common/DataTable';
import Layout from '@/components/layout/Layout';

const usersData = [
  {
    id: 1,
    name: 'John Doe',
    email: 'john@example.com',
    department: 'IT',
    role: 'Admin',
    status: 'Active',
  },
  // ... autres utilisateurs
];

const columns = [
  { key: 'name', label: 'Nom', sortable: true },
  { key: 'email', label: 'Email', sortable: true },
  { key: 'department', label: 'Département', sortable: true },
  { key: 'role', label: 'Rôle', sortable: true },
  {
    key: 'status',
    label: 'Statut',
    sortable: true,
    render: (item) => (
      <span
        className={`px-2 py-1 rounded-full text-xs ${
          item.status === 'Active' ? 'bg-green-100 text-green-800' : 'bg-red-100 text-red-800'
        }`}
      >
        {item.status}
      </span>
    ),
  },
];

const UsersPage = () => {
  const [users, setUsers] = useState(usersData);

  const handleAddUser = () => {
    // TODO: Implement add user modal
    console.log('Add user clicked');
  };

  const handleEditUser = (user) => {
    // TODO: Implement edit user modal
    console.log('Edit user:', user);
  };

  const handleDeleteUser = (user) => {
    if (window.confirm(`Voulez-vous vraiment supprimer l'utilisateur ${user.name} ?`)) {
      setUsers(users.filter((u) => u.id !== user.id));
    }
  };

  return (
    <Layout title="Utilisateurs">
      <div className="p-6">
        <div className="mb-8">
          <h1 className="text-2xl font-bold text-gray-900">Gestion des Utilisateurs</h1>
          <p className="text-gray-500 mt-1">Administration des comptes et permissions</p>
        </div>

        <DataTable
          data={users}
          columns={columns}
          onAdd={handleAddUser}
          onEdit={handleEditUser}
          onDelete={handleDeleteUser}
          addButtonLabel="Ajouter un utilisateur"
        />
      </div>
    </Layout>
  );
};

export default UsersPage;
