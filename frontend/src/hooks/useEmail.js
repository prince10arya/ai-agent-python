import { useEmailStore } from '../store/useEmailStore';
import { emailService, templateService, ttsService } from '../services/api';

export const useEmail = () => {
  const store = useEmailStore();

  const showMessage = (text, type) => {
    store.setMessage(text, type);
    setTimeout(() => store.clearMessage(), 5000);
  };

  const fetchEmailHistory = async () => {
    try {
      const response = await emailService.getHistory();
      store.setEmailHistory(response.data);
    } catch (error) {
      console.error('Error fetching email history:', error);
    }
  };

  const fetchTemplates = async () => {
    try {
      const response = await templateService.getAll();
      store.setTemplates(response.data);
    } catch (error) {
      console.error('Error fetching templates:', error);
    }
  };

  const handleDraft = async (e) => {
    e.preventDefault();
    if (!store.recipient.trim() || !store.prompt.trim()) {
      showMessage('Please fill in both recipient and prompt fields', 'error');
      return;
    }
    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(store.recipient)) {
      showMessage('Please enter a valid email address', 'error');
      return;
    }

    store.setLoading(true);
    try {
      const response = await emailService.createDraft({
        recipient: store.recipient,
        prompt: store.prompt,
        tone: store.tone
      });
      store.setDraft(response.data);
      store.setEditedSubject(response.data.subject);
      store.setEditedContent(response.data.content);
      showMessage('Draft generated successfully!', 'success');
    } catch (error) {
      showMessage('Error generating draft: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      store.setLoading(false);
    }
  };

  const handleSend = async (e) => {
    e.preventDefault();
    if (!store.recipient.trim() || (!store.prompt.trim() && !store.draft)) {
      showMessage('Please fill in both recipient and prompt fields', 'error');
      return;
    }

    store.setLoading(true);
    try {
      const response = await (store.draft 
        ? emailService.sendDraft({ recipient: store.recipient, subject: store.editedSubject, content: store.editedContent })
        : emailService.sendEmail({ recipient: store.recipient, prompt: store.prompt, tone: store.tone })
      );
      showMessage(`Email sent successfully to ${response.data.recipient}!`, 'success');
      store.resetForm();
      fetchEmailHistory();
    } catch (error) {
      showMessage('Error sending email: ' + (error.response?.data?.detail || error.message), 'error');
    } finally {
      store.setLoading(false);
    }
  };

  const handleSpeak = async () => {
    if (!store.draft) {
      showMessage('Generate a draft first to hear it', 'error');
      return;
    }

    store.setIsSpeaking(true);
    try {
      const textToSpeak = `Subject: ${store.editedSubject}. Content: ${store.editedContent}`;
      
      const response = await ttsService.speak({
        text: textToSpeak,
        voice: 'af_heart',
        speed: 1.0
      });

      const audioBlob = new Blob([response.data], { type: 'audio/wav' });
      const audioUrl = URL.createObjectURL(audioBlob);
      const audio = new Audio(audioUrl);
      
      audio.onended = () => {
        store.setIsSpeaking(false);
        URL.revokeObjectURL(audioUrl);
      };
      
      audio.onerror = () => {
        store.setIsSpeaking(false);
        showMessage('Error playing audio', 'error');
      };
      
      await audio.play();
    } catch (error) {
      store.setIsSpeaking(false);
      showMessage('TTS service unavailable: ' + (error.response?.data?.detail || error.message), 'error');
    }
  };

  return {
    fetchEmailHistory,
    fetchTemplates,
    handleDraft,
    handleSend,
    handleSpeak,
  };
};
