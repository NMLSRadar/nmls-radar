export interface LoanOfficer {
  id: string;
  nmls_id: number;
  first_name: string;
  last_name: string;
  current_state: string;
  license_status: string;
  current_company_id?: string;
  company?: {
    id: string;
    company_name: string;
    company_nmls: number;
    state: string;
  };
  first_seen_date: string;
  created_at: string;
}

export interface CompanyGrowth {
  id: string;
  company_name: string;
  company_nmls: number;
  state: string;
  officer_count: number;
}

export interface ChangeEvent {
  id: string;
  event_type: "NEW_LICENSE" | "COMPANY_TRANSFER" | "LICENSE_STATUS_CHANGE" | "NEW_STATE_APPROVAL";
  nmls_id: number;
  event_description: string;
  old_value?: string;
  new_value?: string;
  detected_at: string;
  processed_status: string;
}

const BASE_URL = "https://nmls-radar-api.onrender.com/api/v1";

export async function fetchFromAPI(endpoint: string, options: RequestInit = {}) {
  const url = `${BASE_URL}${endpoint}`;
  try {
    const res = await fetch(url, {
      ...options,
      headers: {
        "Content-Type": "application/json",
        "Authorization": "Bearer clerk_test_token_prototype",
        ...options.headers,
      },
    });
    if (!res.ok) {
      throw new Error(`API returned response error status: ${res.status}`);
    }
    return await res.json();
  } catch (err) {
    console.error(`API execution failed for endpoint ${endpoint}:`, err);
    throw err;
  }
}