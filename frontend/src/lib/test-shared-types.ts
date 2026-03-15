// Test file to validate cross-workspace imports from @jornada/shared
import { AssessmentSchema, UserSchema } from '@jornada/shared';

// This file validates that frontend can import types from shared workspace
export function testSharedTypes() {
  const user: UserSchema = {
    id: '1',
    email: 'test@example.com',
    full_name: 'Test User',
    role: 'user'
  };

  const assessment: AssessmentSchema = {
    id: '1',
    user_id: user.id,
    status: 'draft',
    scores: {}
  };

  return { user, assessment };
}
