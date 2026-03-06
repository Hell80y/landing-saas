import { BenefitsBlock } from '@/components/blocks/BenefitsBlock';
import { FAQBlock } from '@/components/blocks/FAQBlock';
import { FinalCTABlock } from '@/components/blocks/FinalCTABlock';
import { HeroBlock } from '@/components/blocks/HeroBlock';
import { PricingBlock } from '@/components/blocks/PricingBlock';
import { SocialProofBlock } from '@/components/blocks/SocialProofBlock';
import { CombinedSpec, LandingBlockType } from '@/lib/types';

const blockRenderer: Record<
  LandingBlockType,
  (spec: CombinedSpec) => JSX.Element
> = {
  HeroBlock: (spec) => (
    <HeroBlock
      headline={spec.content.hero?.headline}
      subheadline={spec.content.hero?.subheadline}
      cta={spec.content.hero?.cta}
      primaryColor={spec.design.primaryColor}
    />
  ),
  BenefitsBlock: (spec) => <BenefitsBlock items={spec.content.benefits} />,
  SocialProofBlock: (spec) => <SocialProofBlock items={spec.content.socialProof} />,
  PricingBlock: (spec) => <PricingBlock items={spec.content.pricing} />,
  FAQBlock: (spec) => <FAQBlock items={spec.content.faq} />,
  FinalCTABlock: (spec) => (
    <FinalCTABlock item={spec.content.finalCta} primaryColor={spec.design.primaryColor} />
  )
};

export function ThemeRenderer({ spec }: { spec: CombinedSpec }) {
  const blocks = spec.page.blocks?.length
    ? spec.page.blocks
    : ['HeroBlock', 'BenefitsBlock', 'SocialProofBlock', 'PricingBlock', 'FAQBlock', 'FinalCTABlock'];

  return (
    <section
      className="space-y-6 rounded-xl border border-zinc-700 p-6"
      style={{
        backgroundColor: spec.design.backgroundColor ?? '#09090b',
        color: spec.design.textColor ?? '#fafafa'
      }}
    >
      {blocks.map((block, index) => (
        <div key={`${block}-${index}`}>{blockRenderer[block](spec)}</div>
      ))}
    </section>
  );
}
