import { useQuery } from '@tanstack/react-query';
import { Link} from 'react-router-dom';
import { api } from '../lib/api';

interface FloorPlanSummary {
  id: string;
  name: string;
  building: string;
  floor: string;
}

export function FloorPlansPage() {
  const { data, isLoading, error } = useQuery({
    queryKey: ['floor-plans'],
    queryFn: async () => {
      const { data } = await api.get<FloorPlanSummary[]>('/api/v1/maps');
      return data;
    },
  });

  if (isLoading) return <div className="p-6">Loading...</div>;
  if (error) return <div className="p-6 text-red-600">Error: {String(error)}</div>;

  return (
    <div className="p-6">
      <h1 className="text-2xl font-bold mb-4">Floor Plans</h1>
      
      {data?.length === 0 && <p>No floor plans yet.</p>}
      
      {data?.map((fp) => (
        <div key={fp.id} className="mb-6 p-4 border rounded">
          <h2 className="text-xl font-semibold">{fp.name}</h2>
          <p className="text-gray-600">{fp.building} · Floor {fp.floor}</p>
          <p className="text-sm text-gray-500">ID: {fp.id}</p>
          <Link 
            to={`/floor-plan/${fp.id}`}
              className="text-blue-600 hover:underline text-sm"
          >
            View map →
          </Link>
        </div>
      ))}
    </div>
  );
}