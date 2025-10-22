
exports.getUsers = (req, res, next) => {const users = [
    { id: 1, name: "Mehdi" },
    { id: 2, name: "Sara" },
  ];
  res.status(200).json(users);
};

