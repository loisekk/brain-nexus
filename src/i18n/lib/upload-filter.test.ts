import { describe, expect, it } from "vitest";
import { filterUploadContent } from "./upload-filter";

describe("filterUploadContent", () => {
  it("strips metadata prefix lines", () => {
    const input = [
      "Title: Test",
      "Author: User",
      "Content",
      "This is the actual content.",
    ].join("\n");

    const result = filterUploadContent(input);
    expect(result).toBe("This is the actual content.");
  });

  it("strips URL-only lines", () => {
    const input = [
      "https://example.com",
      "Some text",
      "http://test.com/path",
    ].join("\n");

    const result = filterUploadContent(input);
    expect(result).toBe("Some text");
  });

  it("strips date lines", () => {
    const input = ["2023-10-27", "Content here", "12/31/2022"].join("\n");

    const result = filterUploadContent(input);
    expect(result).toBe("Content here");
  });

  it("handles empty input", () => {
    expect(filterUploadContent("")).toBe("");
  });

  it("handles no filterable lines", () => {
    const input = "Just normal text.\nAnother line.";
    expect(filterUploadContent(input)).toBe(input);
  });
});