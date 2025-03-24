'use client';

import { useState, useEffect } from 'react';
import { Dialog, DialogContent, DialogHeader, DialogTitle, DialogFooter } from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { DropdownMenu, DropdownMenuContent, DropdownMenuItem, DropdownMenuTrigger } from '@/components/ui/dropdown-menu';
import { DotsVerticalIcon } from '@radix-ui/react-icons';
import { format } from 'date-fns';
import { getJournals, createJournal, updateJournal, deleteJournal, type Journal, type JournalResponse } from '@/lib/api';


export function JournalList() {
  const [journals, setJournals] = useState<Journal[]>([]);
  const [currentPage, setCurrentPage] = useState(1);
  const [totalPages, setTotalPages] = useState(1);
  const [searchTerm, setSearchTerm] = useState('');
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);
  const [isViewModalOpen, setIsViewModalOpen] = useState(false);
  const [isEditModalOpen, setIsEditModalOpen] = useState(false);
  const [selectedJournal, setSelectedJournal] = useState<Journal | null>(null);
  const [formData, setFormData] = useState({
    title: '',
    content: '',
    tags: '',
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  const fetchJournals = async () => {
    try {
      setLoading(true);
      const data = await getJournals(currentPage, searchTerm);
      setJournals(data.data);
      setTotalPages(data.total_pages);
      setError(null);
    } catch (error) {
      console.error('Error fetching journals:', error);
      setError('Failed to load journals. Please try again later.');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchJournals();
  }, [currentPage, searchTerm]);

  const handleCreateSubmit = async () => {
    try {
      await createJournal({
        ...formData,
        tags: formData.tags.split(',').map(tag => tag.trim()),
      });
      setIsCreateModalOpen(false);
      setFormData({ title: '', content: '', tags: '' });
      fetchJournals();
    } catch (error) {
      console.error('Error creating journal:', error);
    }
  };

  const handleEditSubmit = async () => {
    if (!selectedJournal) return;
    try {
      await updateJournal(selectedJournal.id, {
        ...formData,
        tags: formData.tags.split(',').map(tag => tag.trim()),
      });
      setIsEditModalOpen(false);
      setSelectedJournal(null);
      setFormData({ title: '', content: '', tags: '' });
      fetchJournals();
    } catch (error) {
      console.error('Error updating journal:', error);
    }
  };

  const handleDelete = async (id: string) => {
    if (!confirm('Are you sure you want to delete this journal entry?')) return;
    try {
      await deleteJournal(id);
      fetchJournals();
    } catch (error) {
      console.error('Error deleting journal:', error);
    }
  };

  const truncateContent = (content: string) => {
    const words = content.split(' ');
    if (words.length <= 50) return content;
    return words.slice(0, 50).join(' ') + '...';
  };

  return (
    <div className="space-y-6">
      <div className="flex justify-between items-center">
        <Input
          type="text"
          placeholder="Search by title or tags..."
          className="max-w-sm"
          value={searchTerm}
          onChange={(e) => setSearchTerm(e.target.value)}
        />
        <Button onClick={() => setIsCreateModalOpen(true)}>Create New Entry</Button>
      </div>

      <div className="space-y-4">
        {journals.map((journal) => (
          <div key={journal.id} className="border rounded-lg p-4 shadow-sm">
            <div className="flex justify-between items-start">
              <div className="space-y-2">
                <h3 className="text-xl font-semibold">{journal.title}</h3>
                <p className="text-gray-600">{truncateContent(journal.content)}</p>
                <div className="flex gap-2">
                  {journal.tags.map((tag) => (
                    <span key={tag} className="bg-gray-100 px-2 py-1 rounded text-sm text-gray-500">
                      {tag}
                    </span>
                  ))}
                </div>
                <p className="text-sm text-gray-500">
                  Updated: {format(new Date(journal.updatedAt), 'MMM d, yyyy')}
                </p>
              </div>
              <div className="flex gap-2">
                <Button variant="outline" onClick={() => {
                  setSelectedJournal(journal);
                  setIsViewModalOpen(true);
                }}>
                  View More
                </Button>
                <DropdownMenu>
                  <DropdownMenuTrigger asChild>
                    <Button variant="ghost" size="icon">
                      <DotsVerticalIcon className="h-4 w-4" />
                    </Button>
                  </DropdownMenuTrigger>
                  <DropdownMenuContent>
                    <DropdownMenuItem onClick={() => {
                      setSelectedJournal(journal);
                      setFormData({
                        title: journal.title,
                        content: journal.content,
                        tags: journal.tags.join(', '),
                      });
                      setIsEditModalOpen(true);
                    }}>
                      Edit
                    </DropdownMenuItem>
                    <DropdownMenuItem onClick={() => handleDelete(journal.id)}>
                      Delete
                    </DropdownMenuItem>
                  </DropdownMenuContent>
                </DropdownMenu>
              </div>
            </div>
          </div>
        ))}
      </div>

      <div className="flex justify-center gap-2 mt-4">
        <Button
          variant="outline"
          disabled={currentPage === 1}
          onClick={() => setCurrentPage(prev => prev - 1)}
        >
          Previous
        </Button>
        <Button
          variant="outline"
          disabled={currentPage === totalPages}
          onClick={() => setCurrentPage(prev => prev + 1)}
        >
          Next
        </Button>
      </div>

      {/* Create Modal */}
      <Dialog open={isCreateModalOpen} onOpenChange={setIsCreateModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Create New Journal Entry</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <Input
              placeholder="Title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
            <Input
              placeholder="Tags (comma separated)"
              value={formData.tags}
              onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
            />
            <Textarea
              placeholder="Content"
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              rows={5}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsCreateModalOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleCreateSubmit}>Submit</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>

      {/* View Modal */}
      <Dialog open={isViewModalOpen} onOpenChange={setIsViewModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>{selectedJournal?.title}</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <div className="flex gap-2">
              {selectedJournal?.tags.map((tag) => (
                <span key={tag} className="bg-gray-100 text-gray-600 px-2 py-1 rounded text-sm">
                  {tag}
                </span>
              ))}
            </div>
            <p className="whitespace-pre-wrap">{selectedJournal?.content}</p>
          </div>
        </DialogContent>
      </Dialog>

      {/* Edit Modal */}
      <Dialog open={isEditModalOpen} onOpenChange={setIsEditModalOpen}>
        <DialogContent>
          <DialogHeader>
            <DialogTitle>Edit Journal Entry</DialogTitle>
          </DialogHeader>
          <div className="space-y-4">
            <Input
              placeholder="Title"
              value={formData.title}
              onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            />
            <Input
              placeholder="Tags (comma separated)"
              value={formData.tags}
              onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
            />
            <Textarea
              placeholder="Content"
              value={formData.content}
              onChange={(e) => setFormData({ ...formData, content: e.target.value })}
              rows={5}
            />
          </div>
          <DialogFooter>
            <Button variant="outline" onClick={() => setIsEditModalOpen(false)}>
              Cancel
            </Button>
            <Button onClick={handleEditSubmit}>Submit</Button>
          </DialogFooter>
        </DialogContent>
      </Dialog>
    </div>
  );
}
