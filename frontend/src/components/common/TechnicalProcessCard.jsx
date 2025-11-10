const TechnicalProcessCard = ({ title, description, icon: Icon, bgColor = 'bg-blue-100', iconColor = 'text-blue-600' }) => (
  <div className="bg-white p-6 rounded-lg shadow-sm">
    <div className="flex items-center space-x-4">
      <div className={`${bgColor} p-3 rounded-full`}>
        <Icon className={`h-6 w-6 ${iconColor}`} />
      </div>
      <div>
        <h3 className="font-semibold text-lg">{title}</h3>
        <p className="text-gray-500 text-sm mt-1">{description}</p>
      </div>
    </div>
  </div>
);

export default TechnicalProcessCard;