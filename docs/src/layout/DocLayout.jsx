import { Outlet } from 'react-router-dom';
import Sidebar from './Sidebar';

export default function DocLayout() {
  return (
    <div className="flex h-screen overflow-hidden">
      <Sidebar />
      <main className="flex-1 overflow-y-auto p-8">
        <div className="max-w-4xl mx-auto doc-content">
          <Outlet />
        </div>
      </main>
    </div>
  );
}
