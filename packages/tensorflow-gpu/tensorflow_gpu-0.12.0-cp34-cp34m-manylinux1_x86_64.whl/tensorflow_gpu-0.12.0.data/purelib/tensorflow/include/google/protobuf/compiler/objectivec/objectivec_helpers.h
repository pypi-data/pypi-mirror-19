// Protocol Buffers - Google's data interchange format
// Copyright 2008 Google Inc.  All rights reserved.
// https://developers.google.com/protocol-buffers/
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

// Helper functions for generating ObjectiveC code.

#ifndef GOOGLE_PROTOBUF_COMPILER_OBJECTIVEC_HELPERS_H__
#define GOOGLE_PROTOBUF_COMPILER_OBJECTIVEC_HELPERS_H__

#include <string>
#include <vector>

#include <google/protobuf/descriptor.h>
#include <google/protobuf/descriptor.pb.h>

namespace google {
namespace protobuf {
namespace compiler {
namespace objectivec {

// Generator options (see objectivec_generator.cc for a description of each):
struct Options {
  Options();
  string expected_prefixes_path;
  string generate_for_named_framework;
  string named_framework_to_proto_path_mappings_path;
};

// Escape C++ trigraphs by escaping question marks to "\?".
string EscapeTrigraphs(const string& to_escape);

// Strips ".proto" or ".protodevel" from the end of a filename.
string StripProto(const string& filename);

// Remove white space from either end of a StringPiece.
void StringPieceTrimWhitespace(StringPiece* input);

// Returns true if the name requires a ns_returns_not_retained attribute applied
// to it.
bool IsRetainedName(const string& name);

// Returns true if the name starts with "init" and will need to have special
// handling under ARC.
bool IsInitName(const string& name);

// Gets the objc_class_prefix.
string FileClassPrefix(const FileDescriptor* file);

// Gets the path of the file we're going to generate (sans the .pb.h
// extension).  The path will be dependent on the objectivec package
// declared in the proto package.
string FilePath(const FileDescriptor* file);

// Just like FilePath(), but without the directory part.
string FilePathBasename(const FileDescriptor* file);

// Gets the name of the root class we'll generate in the file.  This class
// is not meant for external consumption, but instead contains helpers that
// the rest of the classes need
string FileClassName(const FileDescriptor* file);

// These return the fully-qualified class name corresponding to the given
// descriptor.
string ClassName(const Descriptor* descriptor);
string ClassName(const Descriptor* descriptor, string* out_suffix_added);
string EnumName(const EnumDescriptor* descriptor);

// Returns the fully-qualified name of the enum value corresponding to the
// the descriptor.
string EnumValueName(const EnumValueDescriptor* descriptor);

// Returns the name of the enum value corresponding to the descriptor.
string EnumValueShortName(const EnumValueDescriptor* descriptor);

// Reverse what an enum does.
string UnCamelCaseEnumShortName(const string& name);

// Returns the name to use for the extension (used as the method off the file's
// Root class).
string ExtensionMethodName(const FieldDescriptor* descriptor);

// Returns the transformed field name.
string FieldName(const FieldDescriptor* field);
string FieldNameCapitalized(const FieldDescriptor* field);

// Returns the transformed oneof name.
string OneofEnumName(const OneofDescriptor* descriptor);
string OneofName(const OneofDescriptor* descriptor);
string OneofNameCapitalized(const OneofDescriptor* descriptor);

inline bool HasFieldPresence(const FileDescriptor* file) {
  return file->syntax() != FileDescriptor::SYNTAX_PROTO3;
}

inline bool HasPreservingUnknownEnumSemantics(const FileDescriptor* file) {
  return file->syntax() == FileDescriptor::SYNTAX_PROTO3;
}

inline bool IsMapEntryMessage(const Descriptor* descriptor) {
  return descriptor->options().map_entry();
}

// Reverse of the above.
string UnCamelCaseFieldName(const string& name, const FieldDescriptor* field);

enum ObjectiveCType {
  OBJECTIVECTYPE_INT32,
  OBJECTIVECTYPE_UINT32,
  OBJECTIVECTYPE_INT64,
  OBJECTIVECTYPE_UINT64,
  OBJECTIVECTYPE_FLOAT,
  OBJECTIVECTYPE_DOUBLE,
  OBJECTIVECTYPE_BOOLEAN,
  OBJECTIVECTYPE_STRING,
  OBJECTIVECTYPE_DATA,
  OBJECTIVECTYPE_ENUM,
  OBJECTIVECTYPE_MESSAGE
};

enum FlagType {
  FLAGTYPE_DESCRIPTOR_INITIALIZATION,
  FLAGTYPE_EXTENSION,
  FLAGTYPE_FIELD
};

template<class TDescriptor>
string GetOptionalDeprecatedAttribute(const TDescriptor* descriptor, bool preSpace = true, bool postNewline = false) {
  if (descriptor->options().deprecated()) {
    string result = "DEPRECATED_ATTRIBUTE";
    if (preSpace) {
      result.insert(0, " ");
    }
    if (postNewline) {
      result.append("\n");
    }
    return result;
  } else {
    return "";
  }
}

string GetCapitalizedType(const FieldDescriptor* field);

ObjectiveCType GetObjectiveCType(FieldDescriptor::Type field_type);

inline ObjectiveCType GetObjectiveCType(const FieldDescriptor* field) {
  return GetObjectiveCType(field->type());
}

bool IsPrimitiveType(const FieldDescriptor* field);
bool IsReferenceType(const FieldDescriptor* field);

string GPBGenericValueFieldName(const FieldDescriptor* field);
string DefaultValue(const FieldDescriptor* field);
bool HasNonZeroDefaultValue(const FieldDescriptor* field);

string BuildFlagsString(const FlagType type, const vector<string>& strings);

// Builds HeaderDoc/appledoc style comments out of the comments in the .proto
// file.
string BuildCommentsString(const SourceLocation& location,
                           bool prefer_single_line);

// The name the commonly used by the library when built as a framework.
// This lines up to the name used in the CocoaPod.
extern const char* const ProtobufLibraryFrameworkName;
// Returns the CPP symbol name to use as the gate for framework style imports
// for the given framework name to use.
string ProtobufFrameworkImportSymbol(const string& framework_name);

// Checks if the file is one of the proto's bundled with the library.
bool IsProtobufLibraryBundledProtoFile(const FileDescriptor* file);

// Checks the prefix for the given files and outputs any warnings as needed. If
// there are flat out errors, then out_error is filled in with the first error
// and the result is false.
bool ValidateObjCClassPrefixes(const vector<const FileDescriptor*>& files,
                               const Options& generation_options,
                               string* out_error);

// Generate decode data needed for ObjC's GPBDecodeTextFormatName() to transform
// the input into the expected output.
class LIBPROTOC_EXPORT TextFormatDecodeData {
 public:
  TextFormatDecodeData();
  ~TextFormatDecodeData();

  void AddString(int32 key, const string& input_for_decode,
                 const string& desired_output);
  size_t num_entries() const { return entries_.size(); }
  string Data() const;

  static string DecodeDataForString(const string& input_for_decode,
                                    const string& desired_output);

 private:
  GOOGLE_DISALLOW_EVIL_CONSTRUCTORS(TextFormatDecodeData);

  typedef std::pair<int32, string> DataEntry;
  vector<DataEntry> entries_;
};

// Helper for parsing simple files.
class LIBPROTOC_EXPORT LineConsumer {
 public:
  LineConsumer();
  virtual ~LineConsumer();
  virtual bool ConsumeLine(const StringPiece& line, string* out_error) = 0;
};

bool ParseSimpleFile(
    const string& path, LineConsumer* line_consumer, string* out_error);


// Helper class for parsing framework import mappings and generating
// import statements.
class LIBPROTOC_EXPORT ImportWriter {
 public:
  ImportWriter(const string& generate_for_named_framework,
               const string& named_framework_to_proto_path_mappings_path);
  ~ImportWriter();

  void AddFile(const FileDescriptor* file, const string& header_extension);
  void Print(io::Printer *printer) const;

 private:
  class ProtoFrameworkCollector : public LineConsumer {
   public:
    ProtoFrameworkCollector(map<string, string>* inout_proto_file_to_framework_name)
        : map_(inout_proto_file_to_framework_name) {}

    virtual bool ConsumeLine(const StringPiece& line, string* out_error);

   private:
    map<string, string>* map_;
  };

  void ParseFrameworkMappings();

  const string generate_for_named_framework_;
  const string named_framework_to_proto_path_mappings_path_;
  map<string, string> proto_file_to_framework_name_;
  bool need_to_parse_mapping_file_;

  vector<string> protobuf_framework_imports_;
  vector<string> protobuf_non_framework_imports_;
  vector<string> other_framework_imports_;
  vector<string> other_imports_;
};

}  // namespace objectivec
}  // namespace compiler
}  // namespace protobuf
}  // namespace google
#endif  // GOOGLE_PROTOBUF_COMPILER_OBJECTIVEC_HELPERS_H__
