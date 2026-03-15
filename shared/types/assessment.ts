export interface AssessmentSchema {
  id: string;
  user_id: string;
  status: 'draft' | 'completed';
  scores: Record<string, any>;
}
