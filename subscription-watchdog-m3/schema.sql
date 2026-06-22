-- ── Table 1: subscriptions ──────────────────────────────
CREATE TABLE subscriptions (
  id              UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id         TEXT          NOT NULL,

  -- core fields (M2 sends these)
  merchant_name   TEXT          NOT NULL,
  raw_description TEXT,
  price           NUMERIC(10,2) NOT NULL,
  currency        TEXT          NOT NULL DEFAULT 'USD',
  billing_cycle   TEXT          CHECK (billing_cycle IN (
                                  'monthly', 'yearly', 'weekly'
                                )),
  detected_date   DATE          NOT NULL,

  -- enriched fields (M2 sends these — you just store them)
  confidence      NUMERIC(4,3)  CHECK (confidence BETWEEN 0 AND 1),
  category        TEXT          CHECK (category IN (
                                  'streaming', 'saas', 'fitness',
                                  'cloud', 'news', 'gaming',
                                  'food', 'other'
                                )),
  is_recurring    BOOLEAN       DEFAULT TRUE,

  -- M3 manages these internally
  status          TEXT          DEFAULT 'active'
                                CHECK (status IN ('active','cancelled')),
  flagged         TEXT          CHECK (flagged IN (
                                  'price_spike', 'unused',
                                  'duplicate', 'trial_ending', NULL
                                )),
  flag_detail     TEXT,

  -- timestamps
  created_at      TIMESTAMPTZ   DEFAULT NOW(),
  updated_at      TIMESTAMPTZ   DEFAULT NOW()
);

-- ── Table 2: price_history ───────────────────────────────
CREATE TABLE price_history (
  id              UUID          PRIMARY KEY DEFAULT gen_random_uuid(),
  subscription_id UUID          NOT NULL
                                REFERENCES subscriptions(id)
                                ON DELETE CASCADE,
  old_price       NUMERIC(10,2) NOT NULL,
  new_price       NUMERIC(10,2) NOT NULL,
  change_pct      NUMERIC(6,2)  GENERATED ALWAYS AS (
                    ROUND(((new_price - old_price) / old_price) * 100, 2)
                  ) STORED,
  currency        TEXT          DEFAULT 'USD',
  changed_at      TIMESTAMPTZ   DEFAULT NOW()
);

-- ── Table 3: user_prefs ──────────────────────────────────
CREATE TABLE user_prefs (
  user_id              TEXT    PRIMARY KEY,
  alert_threshold_pct  NUMERIC(5,2) DEFAULT 10.00,
  notify_email         TEXT,
  preferred_currency   TEXT    DEFAULT 'USD',
  created_at           TIMESTAMPTZ DEFAULT NOW()
);

-- ── Indexes ──────────────────────────────────────────────
CREATE INDEX idx_subs_user_id ON subscriptions(user_id);
CREATE INDEX idx_subs_status  ON subscriptions(status);
CREATE INDEX idx_subs_flagged ON subscriptions(flagged);
CREATE INDEX idx_ph_sub_id    ON price_history(subscription_id);
