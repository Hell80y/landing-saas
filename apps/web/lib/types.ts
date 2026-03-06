export type LandingBlockType =
  | 'HeroBlock'
  | 'BenefitsBlock'
  | 'SocialProofBlock'
  | 'PricingBlock'
  | 'FAQBlock'
  | 'FinalCTABlock';

export interface CombinedSpec {
  meta: {
    title?: string;
    slug?: string;
  };
  design: {
    theme?: 'light' | 'dark';
    primaryColor?: string;
    backgroundColor?: string;
    textColor?: string;
  };
  content: {
    hero?: {
      headline?: string;
      subheadline?: string;
      cta?: string;
    };
    benefits?: { title: string; description: string }[];
    socialProof?: { quote: string; author: string }[];
    pricing?: { plan: string; price: string; features: string[] }[];
    faq?: { question: string; answer: string }[];
    finalCta?: {
      title?: string;
      description?: string;
      buttonText?: string;
    };
  };
  page: {
    blocks: LandingBlockType[];
  };
  commerce?: Record<string, unknown>;
  tracking?: Record<string, unknown>;
}

export interface Landing {
  id: string;
  name: string;
  status: 'draft' | 'generated' | 'published';
  combined_spec: CombinedSpec;
  created_at?: string;
  updated_at?: string;
}
